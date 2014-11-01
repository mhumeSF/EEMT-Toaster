#!/usr/bin/env python

######################################################################
## slopeaspect.py
## Written by Daniel Spence for the ISTA-420-Midterm project
## for testing and debugging I strongly suggest using this resource:
## http://grasswiki.osgeo.org/wiki/GRASS_and_Python
## usage: python slopeaspect.py elevationRaster=sosierra_warp 
##        slope=slope aspect=aspect
#######################################################################

import sys
# The related files are at $GISBASE/etc/python/grass/script/*.py
import grass.script as grass
from grass.pygrass.modules.shortcuts import raster as r 
from grass.pygrass.modules import Module
	
def main():

	for arg in sys.argv:
		mySplit = arg.split('=')
		if len(mySplit) > 1:
			command = mySplit[0]
			value = mySplit[1]
			print command
			print value
			if command == "elevationRaster":
				elevationRaster = value
			elif command == "slope":
				slope = value
			elif command == "aspect":
				aspect = value
	
	# call r.slope.aspect
	slope_aspect = Module("r.slope.aspect")
	slope_aspect(elevation=elevationRaster, slope=slope,  aspect=aspect, 
               format='degrees', overwrite=True)
	
if __name__ == "__main__":
    main()
			