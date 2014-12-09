#!/usr/bin/python2

from netcdf import *
import sys, os

n = netcdf(2007, {11012,11013,11192,11193}, "tmax")

print n.patchRaster
