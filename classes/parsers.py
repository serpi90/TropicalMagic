#!/usr/bin/env python
import sys
from cone import Cone

class RaysParser:
	def __init__(self,filename):
		self.filename = filename

	def parse(self):
		# Load rays from file "input/rays" into a dictionary
		rays = {}
		raysFile = open( self.filename, "r" )
		for line in raysFile:
			line = line.strip()
			if line != "":
					ray,index = line.split("#")
					ray = map(int, ray.split())
					index = int(index)
					rays[index] = tuple(ray)
		raysFile.close()
		return rays

class ConesParser:
	def __init__(self,filename,rays):
		self.filename = filename
		self.rays = rays

	def parse(self):
		# Load cones from file "input/cones" into a list
		cones = []
		conesFile = open( self.filename , "r" )
		for line in conesFile:
			line = line.strip().replace("\t"," ").strip("{}")
			if line != "":
				indexes = map( int, line.split() )
				rays = {}
				for i in indexes:
					rays[i] = self.rays[i]
				cone = Cone( rays )
				cones.append(cone)
		conesFile.close()
		return cones

class ElementsParser:
	def __init__(self,filename,cones):
		self.filename = filename
		self.cones = cones

	def parse(self):
		elementsFile = open( self.filename, "r" )
		elementsByCone = {}
		for line in elementsFile:
			line = line.strip()
			if line != "":
				elementString,coneString = line.split("#")
				cone = self.parseCone( coneString )
				element = self.parseElement( elementString )
				elementsByCone[cone] = element
		elementsFile.close()
		return elementsByCone

	def parseCone(self, string):
		matchingCones = filter(  lambda each: str(each) == string, self.cones)
		if len(matchingCones) == 0:
			sys.exit("Cone " + string + " not found")
		return matchingCones[0]

	def parseElement(self, string):
		return map( lambda s: -int(s.strip()), string.strip("() ").split(",") )
