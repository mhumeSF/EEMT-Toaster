#!/usr/bin/python2

from netcdf import *
import sys, os



#n = netcdf(1980, [11369, 11370], "tmin")

tiles = [11752, 11751]


print "now testing a single raster area"

n = netcdf(1980, tiles, "tmax")
n = netcdf(1980, tiles, "tmin")
n = netcdf(1980, tiles, "prcp")

print n.patchRaster
