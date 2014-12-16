from geotiff import *

florida = geotiff("dems/calx.output.mean.tif")
center = florida.getCenter()
degrees = florida.toDegrees(center)
print("florida center" + str(degrees))

cali = geotiff("dems/cali.output.mean.tif")
center = cali.getCenter()
degrees = cali.toDegrees(center)
print("cali center" + str(degrees))

brazil = geotiff("dems/brazil.output.mean.tif")
center = brazil.getCenter()
degrees = brazil.toDegrees(center)
print("brazil center" + str(degrees))
