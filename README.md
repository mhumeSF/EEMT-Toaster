Overview of the project
==

Please Read: docker/README.md to setup a docker image and instantiate a container.

Different stages of the project:
* Data collection - Plain Download from OpenTOPO
* Data storage - Store on iPlant? FutureGrid? LAX/LAZ files: compressed Lidar Data.
* Prepare data - temp, pressure, etc data, input time, lat/long to get required data.
* Distribute computations - Use Docker/Makeflow to distribute data across HPC/FG/whatever
* Process data - Use formulae to crunch the numbers
* Prepare output - Each docker instance should write its output to files. Directory structure / file name should reflect the organization of data.
* Output format - All inputs, intermediate results and outputs should be put into a csv/json to let data visualization s/w to work on it
* Visualization - TBD


Data Collection
==
DEM
OpenTopo: Contains the DEM files which contain latlong points.


Data Storage
==
iPlant/XSEDE


Prepare Data
==
* Phase 1: Data will be saved as raster files within the grassdata database specified by the user.
* Phase 2: Data will be stored using iRODS if the user chooses to do so.

Warp Geotiff to LCC projection using gdalwarp
Import GRASS raster from Geotiff


Distribute computations
==
Actual Implementation:
WorkQueue : Create workers to run r.sun calculations for each day of the year.

Original plan:
Docker : use it to containerize our apps so that we can run the docker anywhere.
*UAHPC / PBS distrobution systems* : Currently tested and working.  Script has the ability to distribute tasks in parallel and report back to the user when tasks are complete.


Process Data
==
GRASS : raster map functions to create solar radiation models and localized temperature models *Future products*
QGIS : does some calculations related to water slope models and (maybe) make a predictive analysis of weather change.
EEMT = E_ppt + E_bio (J / (m^2 * s))

Prepare output
==
Output will be staged in the given grassdata database file structure

Output format
==
Raster maps that are included in the given grassdata database file structure

Visualization
==
Under Construction

User Interfaces
==
Under Construction
Entry point python script where the user can:
* specify a folder of geotiff files to work on
* specify a range of years to work on
* specify parameters to calculate EEMT (Tmin, Tmax, swe, dayl, etc..)
* specify a time step to use
* specify monthly averages or daily averages

Application Programming Interface
==
Our python scripts were written with extensibility in mind.  The current goal is to have other scientists work with and use our scripts to meet their own ends, therefore, we thought it was important to create types that others can use to extend or build upon what we currently offer here.  An overview of the API can be found here: [https://github.com/mhumeSF/ISTA-420-Midterm/tree/master/src]
Geotiff Class Interface
==
    init(self, tiff):
    ex: tiff = Geotiff("output.mean.tif")
    Constructor: Initializes a new geotiff object which instance methods can be called on.
    This also generates a GRASS raster which is used for subsequent processes. The raster
    is generated after the geotiff has been warped to the daymet projection and region
    The constructor takes one argument, a link to a geotiff file.

    (Not Used)
    getCenter(self):
    ex: center = tiff.getCenter()
    This method calls gdalinfo on the object's geotiff file.  It parses the 
    output to save the center coordinates of the geotiff. It outputs a tuple 
    of the lon, lat center coordinates of the geotiff.
    
    getCordinates(self):
    ex: corners = tiff.getCorners()
    This method calls gdalinfo on the geotiff file and parses the output to
    acquire the top left and bottom right corner coordinates. The output is
    two tuples, the first being the x,y coordinates of the top left corner of the region and the second being the x,y coordinates of the bottom right
    corner of the region.
    toDegrees(self, coords): ex: decimal = tiff.toDegrees(center)
    This method converts coordinates in day,hour,minute,second format to
    decimal degrees. It takes one argument, a tuple (lat, long) for
    the conversion. It returns decimal degree values as (lat, long)

    (unused)
    forDaymetR(self, coords, sYear=1980, eYear=2015, param="all", outDir="~/DaymetTiles"):
    This method generates the os commands necessary to call DaymetR. It takes 
    one argument; a pair of lat/lon coordinates in the form of a tuple.
    The first lat/lon values are the top left corner of the selected region
    and the second two are the bottom left corner of the region. It then
    makes an os call for DaymetR which grabs tiles using the lat lon values.
    
    def toMatrix(self, coords):
    This method converts coordinates in decimal lat/lon format into the proper
    format to query the tile number matrix that we have built. It takes one
    argument, a tuple, which is a pair of lat/lon coordinates and returns the
    local matrix indices corresponding to the coords. These can be used to 
    lookup the index of tile IDs.

    def getTiles(self, coords):
    This method takes in (UL LR) as a space-delimited coordinates in a tuple and 
    returns the list of tiles that are contained in this rectangular geographical area.
    
    def getTileList(self, indices):
    This method takes in 2x(i,j) indices and returns a list of tiles that 
    encompass those indices.
    
    def gdalwarp(self, input, output):
    This method calls gdalwarp on its argument to warp the coordinates of the
    geotiff file to the new coordinate system. It outputs a geotiff file.
    The two arguments are filenames to an input geotiff file and an output
    geotiff file. 

Raster Class Interface
==
    init(self, tiff, raster):
    ex: ras = raster("output.mean.tif", "./raster")
    Constructor: Initializes a new instance of a raster object and sets
    the g.region for concurrent raster calculations. It takes two
    arguments, the first is an input geotiff file, the second is a
    name for an output raster file.

    (unused)
    export(self, raster, output):
    ex: ras.export("output.mean.tif", "./raster")
    This method exports the raster files using the command r.external and
    g.region. It takes two arguments, the first is a raster and the second
    is the name is the geoTiff to output as.

    slopeAspect(self, elevationRaster, outputSlope, outputAspect):
    ex: ras.slopeAspect("MyElevRast", "MySlope", "MyAspect")
    This method calls the r.slope.aspect function from the grass module.
    It takes three arguments, the first of which is an input elevation raster
    file, the second is an output name for a slope file and the third is an
    output name for an aspect file.

    sun(self, myElevRaster, mySlope, myAspect, myDay, myStep, myInsol_time, myGlob_rad):
    ex: ras.sun(myElevRaster, mySlope, myAspect, myDay, myStep, myInsol_time, myGlob_rad)
    This method calls the r.sun function from the grass module. There are a
    ton of arguments for it to run properly.

    mapCalc(self, param, paramRaster, rasterOut, elevRaster, daymetRaster):
    ex: ras.mapCalc(tmin, paramRaster, rasterOut, elevRaster, daymetRaster)
    This method calls the r.mapcalc function from the grass module. Its output
    is based on which parameter type is specified. Different calculations are
    done depending on the parameter, currently tmin and tmax.

