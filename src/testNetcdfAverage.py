#!/usr/bin/python2

from netcdfAverage_local import *
import sys, os



#n = netcdf(1980, [11369, 11370], "tmin")

tiles = [11751]
years = range(1980,1983)
param = "tmax"

print "now testing a single raster area"

n = netcdf()

n.process(years, tiles, param)
n.averageRasters()

print n.patchRaster
