#!/usr/bin/env python

######################################################################
## sun.py
## Written by Daniel Spence for the ISTA-420-Midterm project
## for testing and debugging I strongly suggest using this resource:
## http://grasswiki.osgeo.org/wiki/GRASS_and_Python
## usage: python sun.py elevationRaster=elevationRaster slope=slope 
##        aspect=aspect day=day step=step beam_rad=beam_rad 
##        isol_time=insol_time diff_rad=diff_rad refl_rad=refl_rad 
##        glob_rad=glob_rad
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
			if command == "elevationRaster":
				myElevationRaster = value
			elif command == "slope":
				mySlope = value
			elif command == "aspect":
				myAspect = value
			elif command == "day":
				myDay = value
			elif command == "step":
				myStep = value
			elif command == "beam_rad":
				myBeam_rad = value
			elif command == "insol_time":
				myInsol_time = value
			elif command == "diff_rad":
				myDiff_rad = value
			elif command == "refl_rad":
				myRefl_rad = value
			elif command == glob_rad":
				myGlob_rad = value
	
	
	# call r.sun
	r.sun(elevationRaster=myElevationRaster, slope=mySlope,
	      aspect=myAspect, day=myDay step=myStep, beam_rad=myBeam_rad,
		  insol_time=myInsol_time, diff_rad=myDiff_rad, refl_rad=myRefl_rad,
		  glob_rad=myGlob_rad flags="s" overwrite=true)
		  
	
	
if __name__ == "__main__":
    main()
			