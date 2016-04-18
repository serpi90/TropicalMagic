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

generatorsFile = open( "output/generators.txt", "w" )
for cone in cones:
 	generatorsFile.write( str(cone) + "\t=>" )
	for ray in cone.rays():
		possibleCone = filter( lambda r: r != ray, cone.rays())
		rayToVector = lambda r: reduce( lambda x,y : "%s,%s" % (x,y), r )
		singularFile = open("cone.singular", "w")
		singularFile.write('LIB"gfanlib.so";\n')
		singularFile.write("intmat points[%s][%s] =\n\t" % (len(possibleCone),len(ray)) )
		singularFile.write(",\n\t".join(map( rayToVector, possibleCone)) + ";\n")
		singularFile.write("cone c = coneViaPoints(points);\n")
		singularFile.write("intvec r = %s;\n" % rayToVector(ray))
		singularFile.write("containsInSupport(c,r) || containsRelatively(c,r);\n")
		singularFile.close();
		isRayInPossibleCone = bool(int(subprocess.check_output("Singular -bq < cone.singular", shell=True).strip()))
		os.system("rm -f cone.singular")
		if isRayInPossibleCone:
			cone.removeRay( ray )
 	generatorsFile.write( str(cone) + "\n" )
generatorsFile.close()
