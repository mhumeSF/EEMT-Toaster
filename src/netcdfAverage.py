#!usr/bin/python2

import os, sys, urllib2
from workQ import *
from grassData import *

class netcdf:

    def __init__(self, workQueueObject, param):
        """
        Constructor: takes a workqueue object as arg to be used for the rest of the class
        """
        self.wq = workQueueObject
        self.param = param
        self.tag_name = "netcdf_download"
        self.taskids = []

        # Create a netcdfs folder if it isn't there to store the netcdfs downloaded from Daymet
        if not os.path.exists ("netcdfs"):
            os.mkdir ("netcdfs")

    def get_tag_name (self):
        return self.tag_name

    def get_average_tag (self):
        return self.average_tag

    def get_taskids (self):
        return self.taskids

    def process (self, years, tiles):
        """
        This method takes three arguments, list of years, a list of tiles, and a parameter.
        It then calls all of the instance methods on the current object. It is a main method of sorts.
        """
        self.years = years
        self.tiles = tiles
        # ! ! ! ! ! ! ! ! ! ! ! ! !
        # TODO
        self.days = range(1,11)
        self.rasters = []
        self.maps = []

        for tile in self.tiles:
            for year in self.years:
                self.maps.append( "netcdfs/" + str(self.param) + "_" + str(year) + "_" + str(tile) )

                if len(self.tiles) > 1:
                    self.rasters.append( str(self.param) + "_" + str(year) + "_" + str(tile) )
                else:
                    self.rasters.append( str(self.param) + "_" + str(year) )

        print self.rasters
        #set the projection and clear up g:
        command = "g.proj -c proj4=\"+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs\""
        os.system(command)
        self.getNetcdf()

    def getNetcdf(self):
        """
        This method uses wget to acquire netCdf files from the thredds file server. It gets a netCdf for each tile
        and downloads them all into the local path. If a file with the same name is found in the current directory,
        downloading of the file is skipped assuming that the file has already been downloaded.
        """
        print ("saving in directory: " + os.getcwd())
        for tile in self.tiles:
            for year in self.years:
                filename = "netcdfs/" + self.param + "_" + str(year) + "_" + str(tile) + ".nc"

                url = ("http://thredds.daac.ornl.gov/thredds/fileServer/ornldaac/1219/tiles/%d/%d_%d/%s.nc") % \
                    (year, tile, year, self.param)

                command = ("wget --waitretry=10 --limit-rate=1000k -t 0 -O %s %s") % (filename, url)

                # Check if file already exists and the size matches that of content-length from url head
                if self.netcdfExists(url, filename):
                    print filename + ": File Exists. Skipping Download..."
                else:
                    # arg1 -> tag_name
                    # arg2 -> list of strings : [command, num_inputs, <input file names>, num_outputs, <output file names>
                    taskid = self.wq.wq_job(self.tag_name, [command, "0", "1", filename])
                    self.taskids.append(taskid)

    def netcdfExists(self, url, filename):
        """
        Verifies netCDF is downloaded to it's entirety by verifying the filesize with the content-length header
        """
        return (os.path.isfile (filename)) and (int(os.path.getsize(filename)) == int(urllib2.urlopen(url).headers['content-length']))


    def averageRasters(self):

        self.taskids = []
        self.toRaster()

        return
        if len(self.tiles) > 1:
            self.rasterPatch()
        else:
            self.patchRaster = self.rasters[0]

        self.tag_name = "netcdf_average"
        os.system("g.region rast=" + self.param + "." + str(self.days[0]))

        outputRasters = []
        inputRasters = []
        for day in self.days:

            inputRaster = self.param + "." + str(day)
            command = "r.mapcalc \"" + inputRaster + "=("
            first = True
            for year in self.years:
                raster = self.param + "_" + str(year)

                if first:
                    command += raster + "." + str(day)
                    first = not(first)
                else:
                    command += "+" + raster + "." + str(day)
            command += ")/" + str(len(self.years)) + "\""

            taskid = self.wq.wq_job(self.tag_name, [command, "0", "0"])
            self.taskids.append(taskid)
            # os.system(command)

    def rasterPatch(self):
        """
        This method uses r.patch to patch all the raster files together.
        The output will be raster files formatted "param_year.day"
        """
        taskids = []
        self.tag_name = "netcdf_patch"
        rastersWithDay = []
        for raster in self.rasters:
            rastersWithDay.append(raster + ".1")

        myRegionInput = ",".join(rastersWithDay)

        command = "g.region rast=" + myRegionInput

        try:
            os.system(command)
        except:
            print "rasterPatch command did not complete"

        # iterate through all days of the year
        for i in self.days:
            for year in self.years:
                rasterWithDay = []
                for raster in self.rasters:
                    rasterWithDay.append( raster + "." + str(i) )

                myRasterInput = ",".join(rasterWithDay)
                myRasterOutput = str(self.param) + "_" + str(year)

                command = "r.patch input=" + myRasterInput + " output=" + myRasterOutput + "." + str(i) + " --overwrite"
                #print command
                #patched raster outputs will be "param_year.day"
                try:
                    #os.system(command)
                    taskid = self.wq.wq_job(self.tag_name, [command, "0", "0"])
                    taskids.append(taskid)

                except:
                    print "rasterPatch command did not complete"
                self.patchRaster = myRasterOutput
        self.wq.wq_wait(self.tag_name, taskids)

    def toRaster(self):
        """
        This method uses the r.external command to convert .nc files to raster files. It creates a new raster
        for each day (band) within the netcdf input. Each band is separated by a period ie. "tmin_1980_11369.365".
        """
        i = 0
        for mp in self.maps:
            # save it as the same file name to save space
            command = "gdal_translate -of GTiFF NETCDF:" + mp + ".nc " + mp + ".nc"
            print command
            try:
                os.system(command)
            except:
                print "toRaster command did not complete"

            command = "r.external -o input=" + mp + ".nc output=" + self.rasters[i] +" --overwrite"
            # print command
            i+=1
            try:
                os.system(command)
            except:
                print "toRaster command did not complete"

        return
