class netcdf:

    def __init__(self):
        self.rasters = []


    """
    This be where I use that wet get command to grab images off the intertubes
    """
    def getNetcdf(self, year, tileId):
        command = "wget http://thredds.daac.ornl.gov/thredds/fileServer/ornldaac/1219/tiles/" \
                    + year + "/" + tileid + "_" + year + "/" + param + ".nc"
        try:
            os.system(command)
        except:
            print "netcdf command did not complete"


    """
    I patch all the rasters
    """
    def rasterPatch(self, outputRaster):
        myRasterInput = " ".join(self.rasters)
        command = "r.patch " + myRasterInput + " " + outputRaster

    def toRaster(self):
        gdal_translate -of GTiFF NETCDF:tmin.nc -b 365 myAwesomeNetCDF
        return

    # netcdf_raster_year_day_a
    # netcdf_raster_year_day_b

    # patch a+b to produce patched raster
