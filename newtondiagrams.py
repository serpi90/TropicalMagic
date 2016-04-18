#!/usr/bin/env python
import operator
import os
import argparse

from classes.parsers import RaysParser
from classes.parsers import ConesParser
from classes.parsers import ElementsParser
from classes.cone import Cone
from classes.outputs import ExcelOutput
from classes.outputs import PrintOutput

parser = argparse.ArgumentParser()
parser.add_argument('--plot', required=False, action='store_true')
parser.add_argument('--excel', required=False, action='store_true')
parser.add_argument('--quiet', required=False, action='store_true')
args = parser.parse_args()

class DontPlotCommand:
	def plot(self, cone, element, sides):
		pass

class PlotCommand:
	def __init__(self, outputPath):
		self.outputPath = outputPath

	def prepare(self):
		if not os.path.exists(self.outputPath):
		    os.makedirs(self.outputPath)

	def plot(self, cone, element, sides):
		points = list(enumerate(element))
		pointsFile = open("points.dat", "w")
		for x in points:
			pointsFile.write("%i %i\n" % tuple(x))
		pointsFile.close()
		lowerFile = open("lower.dat", "w")
		for side in sides:
			for x in side:
				lowerFile.write("%i %i\n" % tuple(points[x]))
		lowerFile.close()
		filename = self.outputPath + "/" + reduce( lambda x,y: "%s-%s" % (x,y), cone.indexes()) + ".png"
		os.system("gnuplot < plot.gnuplot; mv plot.png " + filename  )
		os.system("rm -f lower.dat points.dat")

outputs = []
if not args.quiet:
	outputs.append( PrintOutput() )
if args.plot:
	plotCommand = PlotCommand("output/diagrams")
	plotCommand.prepare()
else:
	plotCommand = DontPlotCommand()
if args.excel:
	outputs.append( ExcelOutput("output/Results.xlsx", ["Type", "Hidden Ties", "Lower Hull", "Rays", "Cone"] ) )

# Obtain the lower hull of a set of points
def lower_hull(points):
	points = sorted(set(points))

	# Boring case: no points or a single point, possibly repeated multiple times.
	if len(points) <= 1:
		return points

	# 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
	def cross(o, a, b):
		return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

	# Build lower hull
	lower = []
	for p in points:
		while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
			lower.pop()
		lower.append(p)

	return lower

# Obtain the slope between 2 points
def slope(a, b):
	return float(a[1]-b[1]) / float(a[0]-b[0])

def categorize( sides, points ):
	lengths = filter( lambda x: len(x)>2,  sides)
	length3 = filter( lambda x: len(x)==3, sides)
	length4 = filter( lambda x: len(x)==4, sides)
	if ( len(length3) == 2 ) and ( len(lengths) == 2 ):
		return 1
	elif ( len(length4) == 1 ) and ( len(lengths) == 1 ):
		return 2
	elif ( len(length3) == 1 ) and ( len(lengths) == 1 ):
		return 3
	else:
		return "?"

def findHiddenTies( sides, points ):
	# We assume the cone is type 3
	length3 = filter( lambda x: len(x)==3, sides)
	first = points[length3[0][0]]
	last = points[length3[0][2]]
	s = slope(first,last)
	draws = []
	possible_draws = filter( lambda x: length3[0].count(x[0])==0, points )
	for i in range( 0, len(possible_draws)-1 ):
		for j in range( i+1, len(possible_draws) ):
			if slope(possible_draws[i],possible_draws[j]) == s:
				draws.append((possible_draws[i][0],possible_draws[j][0]))
	return draws

def findLowerHullSides( points, lower ):
	i,j = 0,0
	sides = []
	while i < len(points) - 1:
		# If the current point (i) is in the hull, then we add it to the result, and get the next slope.
		if points[i] == lower[j]:
			if j > 0:
				sides[j-1].append(i)
			sides.append([i])
			s = slope(lower[j],lower[j+1])
			j = j + 1
		# If the slope between the last known point in the hull (j) and the current point (i)
		# matches the slope between the (j) and the next point in the hull (j+1)
		# then (i) is in the edge of the hull so we add it to the result.
		elif slope(lower[j],points[i]) == s:
			sides[j-1].append(i)
		i = i + 1

	# The rightest element is always in the hull.
	sides[len(sides)-1].append(len(points)-1)
	return sides

# Read the elements and cones from "output/elements.txt"
# Since we are going to use the lower hull instead of the upper hull, the elements are negated.
rays = RaysParser("input/rays").parse()
cones = ConesParser("input/cones",rays).parse()
elementsByCone = ElementsParser("output/elements.txt",cones).parse()
map(lambda output: output.start(), outputs)

for cone in elementsByCone.keys():
	element = elementsByCone[cone]
	points = list(enumerate(element))
	lowerHull = lower_hull(points)
	sides = findLowerHullSides(points, lowerHull)

	# Output the result
	coneType = categorize(sides, points)
	hiddenTies = []
	if coneType == 3:
		hiddenTies = findHiddenTies( sides, points )

	plotCommand.plot( cone, element, sides )
	for output in outputs:
		output.write( [coneType, hiddenTies, sides, element, cone] )

map(lambda output: output.stop(), outputs)
