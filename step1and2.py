#!/usr/bin/env python
import random
import operator
import os

# Load rays from file "input/rays" into a dictionary 
rays = {}
raysFile = open( "input/rays", "r" )
for line in raysFile:
	line = line.strip()
	if line != "":
			ray,index = line.split("#")
			ray = map(int, ray.split())
			index = int(index)
			rays[index] = tuple(ray)
raysFile.close()

# Load cones from file "input/cones" into a list
conesFile = open( "input/cones" , "r" )
cones = []
for line in conesFile:
	line = line.strip().replace("\t"," ").strip("{}")
	if line != "":
		cone = tuple(map( int, line.split() ))
		cones.append( cone )
conesFile.close()

# Use a fixed for the random  numbers, so we can reproduce the calculations
random.seed(42)

# Function that multiplies a ray with a pseudo-random integer in range [1, 1000]
def randomFactor( ray ):
	r = random.randrange( 1, 1000 )
	return map( lambda x: x*r, ray )

# Load the reduced_grobner_base to use as header for the output files
headerFile = open( "input/reduced_grobner_base" )
header = headerFile.read()
headerFile.close()

# Generate the zero point, with the same length as the rays => (0,0,0,0,0,0)
zero = tuple( [0] * len(rays[0]) )

if not os.path.exists("output/elements"):
    os.makedirs("output/elements")
# Generate an element from each cone, log it to "elements.txt" and generate the output file "x-x-x-x.step2"
elementsFile = open( "output/elements.txt", "w" )
for cone in cones:
	element = zero
	for rayindex in cone:
		element = tuple(map( operator.add, randomFactor(rays[rayindex]), element ))
	elementsFile.write( str(element) + " #" + str(cone) +"\n" )
	elementFile = open( "output/elements/" + str(cone).replace(",","-").replace(" ","").strip("()") + ".step2", "w" )
	elementFile.write( header )
	elementFile.write( str(element) )
	elementFile.write( "\n\n" )
	elementFile.write("# Cone: " + str(cone) +"\n" )
	for ray in cone:
		elementFile.write("# Ray: " + str(rays[ray]) +"\n" )
	elementFile.close()
elementsFile.close()

