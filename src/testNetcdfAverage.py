#!/usr/bin/python2

from netcdfAverage import *
import sys, os



#n = netcdf(1980, [11369, 11370], "tmin")

tiles = [11751]
years = range(1980,1995)
param = "prcp"

print "now testing a single raster area"

n = netcdf(years, tiles, param)


print n.patchRaster
