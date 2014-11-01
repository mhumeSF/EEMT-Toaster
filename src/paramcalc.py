#!/usr/bin/env python

######################################################################
## paramcalc.py
## Written by Daniel Spence for the ISTA-420-Midterm project
## for testing and debugging I strongly suggest using this resource:
## http://grasswiki.osgeo.org/wiki/GRASS_and_Python
## usage: python paramcalc param=tmin paramValue=$tmin 
##        rasterout=tmin_loc elevationRaster=sosierra_warp 
##        daymetRaster=na_dem
#######################################################################

import sys
# The related files are at $GISBASE/etc/python/grass/script/*.py
import grass.script as grass
from grass.pygrass.modules.shortcuts import raster as r 
	
def main():
	for arg in sys.argv:
		mySplit = arg.split('=')
		if len(mySplit) > 1:
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
		lapseRate = 5.69
		tmin = paramValue
		r.mapcalc( "%s = %f-(%f/1000*(%s-%s))" % rasterout, tmin, lapseRate, elevationRaster, daymetRaster )
	if param == "tmax":
		lapseRate = 5.69 # is this the same for tmax?
		tmax = paramValue
		r.mapcalc( "%s = %f-(%f/1000*(%s-%s))" % rasterout, tmax, lapseRate, elevationRaster, daymetRaster )
	else:
		print "Invalid param type"
	
	#TODO: Add the rest of the equations for each parameter
	
if __name__ == "__main__":
    main()
	