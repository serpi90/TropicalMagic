#!/usr/bin/env python
import operator
import os

# Load rays from "input.txt" file and, format it for singular and write it to "output.txt" file
inputFile = open( "input.txt", "r" )
content = inputFile.read()
content = content.replace("Q[","ring R=0, (T,").replace("]","), dp;").replace("{","vector f=[").replace("}","];")

outputFile = open( "output.txt", "w" )
outputFile.write(content)
outputFile.close()

