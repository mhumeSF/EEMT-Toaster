from geotiff import *

for i in ("florida","cali","na_dem"):
    locn = geotiff("../dems/" + i + ".output.mean.tif")
    coords = locn.getCoordinates()
    degrees = locn.toDegrees(coords)
    print (locn.getTiles (degrees))
