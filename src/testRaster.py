#!/usr/bin/python
from raster import *

print "Testing raster constructor using ../dems/brazil.output.mean.tif and myRaster"
r = raster("../dems/cali.output.mean.tif", "myRaster")

print "Testing slopeAspect using myRaster, slope and aspect"
r.slopeAspect("myRaster", "slope", "aspect")

print "Testing sun using myRaster, slope and aspect, insol_raster and glob_raster"
r.sun("myRaster", "slope", "aspect", "1", "0.05", "insol_raster", "glob_raster")

print "Testing parameter mapcalc..."
r.mapcalc("tmin", "myRaster", "calcRaster", "myRaster", "myRaster")
