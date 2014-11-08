#!/usr/bin/python

from geotiff import *

tiff = geotiff("../dems/florida.output.mean.tif")
coords = tiff.getCoordinates()
print("coordinates = " + str(coords))
coords = tiff.toDegrees(coords)
print("decimal = " + str(coords))
tiff.forDaymetR(coords, sYear=1980, eYear=1981, param="tmin", outDir="~/DaymetTiles")
