## Start Here
starthere.py : This script takes a bunch of params, years, filenames as arguments in any insane order and tries to make sense of what they are and use them somehow. 
```
./starthere.py 1525 ../dems/cali.output.mean.tif tmin tmax 8965 ../dems/florida.output.mean.tif -9556    2011      eer ../dems/brazil.output.mean.tiff
                ^                ^                ^     ^    ^             ^                       ^       ^        ^          ^
            invalid yr        valid tif file   valid params  invalid     valid tiff file         inv    valid      junk     invalid file
```

This script also contains "is_tiff_file(filename)" function which returns True if the argument exists as a file and is a valid TIFF file.

## Raster Class Interface

```
init(tiff, raster)
```

This initializes a new instance of a raster object and setsthe g.region for concurrent raster calculations. It takes two arguments, the first is an input geotiff file, the second is a name for an output raster file.

```
export(raster, output)
```

This exports the raster files using the command r.external and g.region. It takes two arguments, the first is a raster and the second is the name of the geoTiff to output as.
        
```
slopeAspect(elevationRaster,slope,aspect)
```

This method calls the r.slope.aspect function from the grass module. It takes three arguments, the first of which is an input elevation raster file, the second is an output name for a slope file and the third is an output name for an aspect file.

```
sun(myElevRaster, mySlope, myAspect, myDay, myStep, myInsol_time, myGlob_rad)
```

This method calls the r.sun function from the grass module. There are a ton of arguments for it to run properly.

```
mapcalc(param, paramRaster, rasterOut, elevRaster, daymetRaster)
```

This method calls the r.mapcalc function from the grass module. Its output is based on which parameter type is specified. Different calculations are done depending on the parameter

## GeoTiff Class Interface
```
init():
ex: tiff = Geotiff("output.mean.tif")
``` 

Initializes a new geotiff object.
Takes one argument, a link to a geotiff file.

```
getCenter():
ex: center = tiff.getCenter()
```

This method calls gdalinfo on the object's geotiff file.  It parses the 
output to save the center coordinates of the geotiff. It outputs a tuple 
of the lon, lat center coordinates of the geotiff.

```
getCordinates():
ex: corners = tiff.getCorners()
```

This method calls gdalinfo on the geotiff file and parses the output to
acquire the top left and bottom right corner coordinates. The output is
two tuples, the first being the x,y coordinates of the top left corner
of the region and the second being the x,y coordinates of the bottom right
corner of the region.

```
toDegrees(coords):
ex: decimal = tiff.toDegrees(center)
```

This method converts coordinates in day,hour,minute,second format to
decimal degrees. It takes one argument, a tuple (lat, long) for
the conversion. It returns decimal degree values as (lat, long)

```
toMatrix()
ex: 
```

This method converts coordinates in decimal lat/lon format into the proper 
format to query the tile number matrix that we have built. It takes one
argument, a tuple, which is a pair of lat/lon coordinates and returns the
local matrix indices corresponding to the coords. These can be used to 
lookup the index of tile IDs.

```
getTiles(coords)
```

This method takes in (UL LR) as a space-delimited coordinates in a tuple and  returns the list of tiles that are contained in this rectangular geographical area.

```
getTileList(indicies)
```

This method takes in 2x(i,j) indices and returns a list of tiles that encompass those indices.
    
```
gdalwarp():
ex: warped = tiff.gdalwarp(...)
```

This method warps the geotiff object into the coordinate system specified as and argument. The method 
