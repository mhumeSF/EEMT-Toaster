#!/usr/bin/python2

from netcdf import *
import sys, os



n = netcdf(1980, [11369, 11370], "tmin")




print "now testing a single raster area"

n = netcdf(1980, [11371], "tmax")
n = netcdf(1980, [11371], "tmin")
n = netcdf(1980, [11371], "prcp")

print n.patchRaster
