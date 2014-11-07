from geotiff import *

tiff = geotiff("../dems/florida.output.mean.tif")
coords = tiff.getCoordinates()
print("coordinates = " + str(coords))
print("decimal = " + str(tiff.toDegrees(coords)))
