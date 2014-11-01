#!/usr/bin/env python

######################################################################
## Written by Daniel Spence for the ISTA-420-Midterm project
## for testing and debugging I strongly suggest using this resource:
## http://grasswiki.osgeo.org/wiki/GRASS_and_Python
## usage: python paramcalc param=tmin paramValue=$tmin 
##        rasterout=tmin_loc elevationRaster=sosierra_warp 
##        daymetRaster=na_dem
#######################################################################

import grass.script as grass
import sys
# this will allow us to natively call r.mapcalc
from grass.pygrass.modules.shortcuts import raster as r 
 

	
def main():
	for arg in argv:
		mySplit = arg.split('=')
		command = mySplit[0]
		value = mySplit[1]
		if command == "param":
			param = value
		elif command == "paramValue":
			paramValue = value
		elif command == "rasterout":
			rasterout = value
		elif command == "elevationRaster":
			elevationRaster = value
		elif command == "daymetRaster":
			daymetRaster = value

	if param == "tmin":
		lapseRate = 5.49
		r.mapcalc( "%s = %f-(%f*(%s-%s/1000))" % rasterout, tmin, lapseRate, elevationRaster, daymetRaster )
	if param == "tmax":
		lapseRate = 5.49 # is this the same for tmax?
		r.mapcalc( "%s = %f-(%f*(%s-%s/1000))" % rasterout, tmax, lapseRate, elevationRaster, daymetRaster )
	else:
		print "Invalid param type"
	
	#TODO: Add the rest of the equations for each parameter
	
	
	
	
	