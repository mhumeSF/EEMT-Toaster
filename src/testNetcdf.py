#!/usr/bin/python2

from netcdf import *
import sys, os




n = netcdf(1980, [11369,11370], "tmin")

print n.patchRaster

print "now testing a single raster area"

n = netcdf(1980, [11371], "tmax")

print n.patchRaster
