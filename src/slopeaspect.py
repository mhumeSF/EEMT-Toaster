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
from subprocess import call
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
                                mySlope = value
                        elif command == "aspect":
                                myAspect = value

        # call r.slope.aspect
		call(["slope.aspect", "elevation=%s" % (elevationRaster), "slope=%s" % (mySlope),
		      "aspect=%s" % (myAspect), "format=degrees", "overwrite=True"])
        #slope_aspect = Module("r.slope.aspect")
        #slope_aspect(elevation=elevationRaster, slope=mySlope,  aspect=myAspect,
        #        format='degrees', overwrite=True)

if __name__ == "__main__":
    main()
