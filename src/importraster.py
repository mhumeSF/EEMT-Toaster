#!/usr/bin/env python

######################################################################
## importraster.py
## Written by Daniel Spence for the ISTA-420-Midterm project
## for testing and debugging I strongly suggest using this resource:
## http://grasswiki.osgeo.org/wiki/GRASS_and_Python
## usage: python importraster.py input=geoTiff output=raster
## description: Creates a raster file and sets the g.region for 
##              Concurrent raster calculations
#######################################################################


import os
import tempfile
from subprocess import call
# python importraster.py input=tiff output=raster


for arg in sys.argv:
		mySplit = arg.split('=')
		if len(mySplit) > 1:
			command = mySplit[0]
			value = mySplit[1]
			if command == "input":
				myInput = value
			if command == "output":
				myOutput = value

call(["r.external", "input=%s" % (myInput), "output=%s" % (myOutput) ])
call(["g.region", "rast=%s" % (myOutput) ])
#r.external(input=myInput, output=myOutput)
#g.region(rast=myOutput)

