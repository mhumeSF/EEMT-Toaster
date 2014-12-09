#!/usr/bin/python2

from netcdf import *
import sys, os




n = netcdf(1980, [11369,11370], "tmin")


print n.patchRaster
