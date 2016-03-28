#!/usr/bin/env python
import operator
import os
import argparse
import xlsxwriter
parser = argparse.ArgumentParser()
parser.add_argument('--plot', required=False, action='store_const', const=True, default=False)
parser.add_argument('--excel', required=False, action='store_const', const=True, default=False)
plot = parser.parse_args().plot
excel = parser.parse_args().excel

if plot:
	os.system("mkdir -p output/diagrams")

# Obtain the lower hull of a set of points
def lower_hull(points):
	points = sorted(set(points))

	# Boring case: no points or a single point, possibly repeated multiple times.
	if len(points) <= 1:
		return points

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
	lengths = filter( lambda x: len(x)>2,  sides )
	length3 = filter( lambda x: len(x)==3, sides)
	length4 = filter( lambda x: len(x)==4, sides)
	if ( len(length3) == 2 ) and ( len(lengths) == 2 ):
		return 1,[]
	elif ( len(length4) == 1 ) and ( len(lengths) == 1 ):
		return 2,[]
	elif ( len(length3) == 1 ) and ( len(lengths) == 1 ):
		first = points[length3[0][0]]
		last = points[length3[0][2]]
		s = slope(first,last)
		draws = []
		possible_draws = filter( lambda x: length3[0].count(x[0])==0, points )
		for i in range( 0, len(possible_draws)-1 ):
			for j in range( i+1, len(possible_draws) ):
				if slope(possible_draws[i],possible_draws[j]) == s:
					draws.append((possible_draws[i][0],possible_draws[j][0]))
		return 3,draws
	else:
		return "?",[]


# Read the elements and cones from "output/elements.txt"
# Since we are going to use the lower hull instead of the upper hull, the elements are negated.
elementsFile = open( "output/elements.txt", "r" )
elements = []
cones = []
for line in elementsFile:
	line = line.strip()
	if line != "":
		element,cone = line.split("#")
		cone = map( lambda s: int(s.strip()), cone.strip("() ").split(",") )
		element = map( lambda s: -int(s.strip()), element.strip("() ").split(",") )
		cones.append( cone )
		elements.append( element )
elementsFile.close()

if excel:
	book = xlsxwriter.Workbook("output/Results.xlsx")
	sheet = book.add_worksheet("Results")
	sheet.write( 0, 0, "Type")
	sheet.write( 0, 1, "Hidden Ties")
	sheet.write( 0, 2, "Lower Hull")
	sheet.write( 0, 3, "Rays")
	sheet.write( 0, 4, "Cone")

for e in range(0, len(elements)):
	element = list(enumerate(elements[e]))
	lower = lower_hull(element)
	i,j = 0,0
	result = []
	while i < len(element) - 1:
		# If the current point (i) is in the hull, then we add it to the result, and get the next slope.
		if element[i] == lower[j]:
			if j > 0:
				result[j-1].append(i)
			result.append([i])
			s = slope(lower[j],lower[j+1])
			j = j + 1
		# If the slope between the last known point in the hull (j) and the current point (i)
		# matches the slope between the (j) and the next point in the hull (j+1)
		# then (i) is in the edge of the hull so we add it to the result.
		elif slope(lower[j],element[i]) == s:
			result[j-1].append(i)
		i = i + 1

	# The rightest element is always in the hull.
	result[len(result)-1].append(len(element)-1)

	# Output the result
	typ,ties = categorize(result, element)
	print "%s\t%s\t%s\t%s\t%s" % (typ, ties, result, map(lambda t: t[1], element), cones[e])
	if excel:
		sheet.write( e+1, 0, str(typ) )
		sheet.write( e+1, 1, str(ties) )
		sheet.write( e+1, 2, str(result) )
		sheet.write( e+1, 3, str(map( lambda t: t[1], element )) )
		sheet.write( e+1, 4, str(cones[e]))

	# If --plot was indicated, then generate the png diagram	
	if plot:
		pointsFile = open("points.dat", "w")
		for x in element:
			pointsFile.write("%i %i\n" % tuple(x))
		pointsFile.close()
		lowerFile = open("lower.dat", "w")
		for x in lower:
			lowerFile.write("%i %i\n" % tuple(x))
		lowerFile.close()
		os.system("gnuplot < plot.gnuplot ; mv test.png output/diagrams/%s.png" % reduce( lambda x,y: "%s-%s" % (x,y), cones[e]) )
		os.system("rm -f lower.dat points.dat")

if excel:
	book.close()
