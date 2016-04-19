#!/usr/bin/env python
import random
import os
import subprocess
from classes.cone import Cone
from classes.parsers import RaysParser
from classes.parsers import ConesParser

# Load rays from file "input/rays" into a dictionary
rays = RaysParser("input/rays").parse()

# Load cones from file "input/cones" into a list
cones = ConesParser("input/generators" , rays ).parse()

def isRayInPossibleCone(ray, cone):
	linealitySpace = [tuple([ 1]*len(ray) ),tuple(range(0, len(ray), 1))]
	possibleCone = filter( lambda r: r != ray, cone.rays())
	singularVector = lambda r: reduce( lambda x,y : "%s,%s" % (x,y), r )
	singularFile = open("cone.singular", "w")
	singularFile.write('LIB"gfanlib.so";\n')
	singularFile.write("intmat points[%s][%s] =\n\t" % (len(possibleCone),len(ray)) )
	singularFile.write(",\n\t".join(map( singularVector, possibleCone)) + ";\n")
	singularFile.write("intmat lineality_space[%s][%s] =\n\t" % (len(linealitySpace),len(ray)) )
	singularFile.write(",\n\t".join(map( singularVector, linealitySpace)) + ";\n")
	singularFile.write("cone c = coneViaPoints(points,lineality_space,1);\n")
	singularFile.write("intvec r = %s;\n" % singularVector(ray))
	singularFile.write("containsInSupport(c,r) || containsRelatively(c,r);\n")
	singularFile.close();
	result = bool(int(subprocess.check_output("Singular -bq < cone.singular", shell=True).strip()))
	os.system("rm -f cone.singular")
	return result

generatorsFile = open( "output/generators.txt", "w" )
generatorsFile.write("# Cones\t=>\tGenerators:\n")
rayindexes = []
for cone in cones:
	generatorsFile.write( str(cone) + "\t=>\t" )
	for ray in cone.rays():
		if isRayInPossibleCone(ray, cone):
			cone.removeRay( ray )
	generatorsFile.write( str(cone) + "\n" )
	rayindexes.extend(cone.indexes())
generatorsFile.write("# Generator Rays: %s\n" % str(sorted(set(rayindexes))))
generatorsFile.close()
