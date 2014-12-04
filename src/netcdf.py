#!usr/bin/python2

import os, sys

class netcdf:
    def __init__(self, year, tiles, param):
        self.year = year
        self.tiles = tiles
        self.param = param
        self.rasters = []
        for tile in tiles:
            self.rasters.append( str(param) + "_" + str(year) + "_" + str(tile) )
        
        #set the projection and clear up g:
        command = "g.proj -c proj4=\"+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs\""
        os.system(command)
        #clear up
        os.system("g.mremove \"*\"")
        
        self.getNetcdf()
        self.toRaster()
        self.rasterPatch()

    def getNetcdf(self):
        """
        This be where I use that wet get command to grab images off the intertubes
        """
        for tile in self.tiles: 
            filename = self.param + "_" + str(self.year) + "_" + str(tile) + ".nc" 
            command = ("wget -O %s http://thredds.daac.ornl.gov/thredds/fileServer/ornldaac/1219/tiles/%d/%d_%d/%s.nc") % \
                    (filename, self.year, tile, self.year, self.param)

            try: 
                if os.path.isfile (filename):
                    print filename + ": File Exists. Skipping Download..."
                else:
                    os.system(command) 
            except: 
                print "netcdf command did not complete"

    def rasterPatch(self):
        """
        I patch all the rasters
        """
        rastersWithDay = []
        for raster in self.rasters:
            rastersWithDay.append(raster + ".1")
        
        myRegionInput = ",".join(rastersWithDay)
        myRasterOutput = str(self.param) + "_" + str(self.year)
        
        command = "g.region rast=" + myRegionInput
        
        try:
            os.system(command)
        except:
            print "rasterPatch command did not complete"
		
        for i in range(1,366):
            rasterWithDay = []
            for raster in self.rasters:
                rasterWithDay.append( raster + "." + str(i) )
            
            myRasterInput = ",".join(rasterWithDay)
            command = "r.patch input=" + myRasterInput + " output=" + myRasterOutput + "." + str(i) + " --overwrite"
            #print command
            #patched raster outputs will be "param_year.day"
            try:
                os.system(command)
            except:
                print "rasterPatch command did not complete"
        
        self.patchRaster = myRasterOutput

    def toRaster(self):
        for raster in self.rasters:
            command = "r.external -o input=" + raster + ".nc" + " output=" + raster +" --overwrite"
            # print command
            try:
				# this will create a raster for each band (or day in this case) within the netcdf input.
				# each band is seperated by a period. ie. "tmin_1980_11369.365"
                os.system(command)
            except:
                print "toraster command did not complete"
        #gdal_translate -of GTiFF NETCDF:tmin.nc -b 365 myAwesomeNetCDF
        return 

    # netcdf_raster_year_day_a
    # netcdf_raster_year_day_b

    # patch a+b to produce patched raster
