#!/usr/bin/env python
import random
import operator

class Cone:
	def __init__(self, generatorRays):
		self.generatorRays = generatorRays

	def getRandomElement(self, generator=random):
		def randomFactor(ray):
			r = generator.randint(1,1000)
			element = tuple(map( lambda x: x*r, ray ))
			return element

		element = tuple( [0] * len(self.rays()[0]) )

		for ray in self.rays():
			element = map( operator.add, randomFactor(ray), element )
		return tuple(element)

	def indexes(self):
		return self.generatorRays.keys()

	def rays(self):
		return self.generatorRays.values()

	def __str__(self):
		return str(self.indexes())

	def removeRay(self, ray):
		for found in filter( lambda item: item[1] == ray, self.generatorRays.items() ):
			del self.generatorRays[found[0]] 
