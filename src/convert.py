#!/usr/bin/python

import sys, math

lat = float(sys.argv[1])
lon = float(sys.argv[2])

lat = (lat-14)/2
lon = (lon+52)/2
print(lat,lon)
lat = math.floor(lat)
lon = math.floor(lon)

print("Our matrix coordinates: " + str(lat) + "," + str(lon))
