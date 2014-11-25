#!usr/bin/python

from netcdf import *
import sys, os

n = netcdf(1980, {11369,11370}, "tmin")

print n.patchRaster