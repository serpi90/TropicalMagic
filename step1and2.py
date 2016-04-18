#!/usr/bin/env python
import random
import os
from classes.cone import Cone
from classes.parsers import RaysParser
from classes.parsers import ConesParser

# Load rays from file "input/rays" into a dictionary
rays = RaysParser("input/rays").parse()

# Load cones from file "input/cones" into a list
cones = ConesParser("input/cones" , rays ).parse()

headerFile = open( "input/reduced_grobner_base" )
header = headerFile.read()
headerFile.close()

# Use a fixed for the random  numbers, so we can reproduce the calculations
randomGenerator = random.Random();
randomGenerator.seed(42)

# Generate an element from each cone, log it to "elements.txt" and generate the output file "x-x-x-x.step2"
if not os.path.exists("output/elements"):
    os.makedirs("output/elements")

elementsFile = open( "output/elements.txt", "w" )
for cone in cones:
	element = cone.getRandomElement(randomGenerator)
	elementsFile.write( str(element) + " #" + str(cone) + "\n" )
	filename = "output/elements/" + str(cone).replace(",","-").replace(" ","").strip("[]() ") + ".step2"
	elementFile = open ( filename, "w" )
	elementFile.write( header )
	elementFile.write( str(element) + "\n\n" )
	elementFile.write("# Cone: " + str(cone) +"\n" )
	for ray in cone.rays():
		elementFile.write("# Ray: " + str(ray) +"\n" )
	elementFile.close()
elementsFile.close()
