from geotiff import *

florida = geotiff("../dems/florida.output.mean.tif")
coords = florida.getCoordinates()
degrees = florida.toDegrees(coords)
print("florida center: " + str(degrees))
matrix = florida.toMatrix(degrees)
print("Matrix coordinates: " + str(matrix))

cali = geotiff("../dems/cali.output.mean.tif")
coords = cali.getCoordinates()
degrees = cali.toDegrees(coords)
print("cali center" + str(degrees))
matrix = florida.toMatrix(degrees)
print("Matrix coordinates: " + str(matrix))

brazil = geotiff("../dems/brazil.output.mean.tif")
coords = brazil.getCoordinates()
degrees = brazil.toDegrees(coords)
print("brazil center" + str(degrees))
matrix = florida.toMatrix(degrees)
print("Matrix coordinates: " + str(matrix))
