#!/usr/bin/python2

import sys, os, subprocess
from toaster import toaster
from netcdfAverage import *
from geotiff import *
from raster import *
from datetime import date
from workQ import *

def is_tiff_file (filename):
    """
    Returns True if the argument exists as a file and is a valid TIFF file
    """
    return os.path.isfile(filename) and "TIFF" in subprocess.check_output("file " + filename, shell=True)

def main ():
    """
    This function takes a bunch of params, years, filenames as arguments in any insane order
    and tries to make sense of what they are and use them somehow.
    """

    # initialize empty lists each for year, params and tiff files gathered from user input
    params_to_use = toaster["params"]
    tiff_files = toaster["dem"]
    years = toaster["years"]
    dem_1km = toaster["na_dem"]
    twi_file = toaster["twi_file"]

    print years
    print params_to_use
    print tiff_files

    netcdfs = []
    wq = workQ()
    nc_objs = []

    for tiff in tiff_files:
        # Find the tile list for a partifular tiff file
        print ("Processing: " + tiff)
        locn = geotiff(tiff)
        coords = locn.getCoordinates()
        degrees = locn.toDegrees(coords)
        tile_list = locn.getTiles (degrees)
        print tile_list

        # Rasterize Topographic Wetness Index
        twiRaster = "twiRaster"
        twi_r = raster(twi_file, twiRaster, wq)

        # Rasterize the dem and distribute slopeaspect
        demRaster = "demRaster"
        r = raster(tiff, demRaster, wq)
        slope = "slope"
        aspect = "aspect"
        r.slopeAspect(demRaster, slope, aspect)

        # Prepare params for r.sun
        myStep = "0.05"
        sun_hours = "sun_hours"
        total_sun = "total_sun"

        # Distribute r.sun and wait for it before eemt calculations
        for day in range(1,20):
            insol_time = sun_hours + "." + str(day)
            glob_rad = total_sun + "." + str(day)
            r.sun(demRaster, slope, aspect, str(day), myStep, insol_time, glob_rad)

        # Now, distribute the downloading of netcdf files
        # Each tile per param is handled as a separate netcdf object
        for param in params_to_use:
            nc = netcdf(wq, param)
            nc_objs.append(nc)
            nc.process(years, tile_list)

        # Wait for netcdf files to be downloaded by the workers
        print "Downloading files . . ."
        for nc in nc_objs:
            wq.wq_wait(nc.get_tag_name(), nc.get_taskids())
        print "Completed Downloading files"

        # Start working on averaging. distribute. Mercilessly
        for nc in nc_objs:
            nc.averageRasters() # cues up more jobs in the nc object -> another wait must be executed

        # Wait.. Wait... W a i t . . . .
        print "Waiting on Converting to Rasters . . ."
        wq.wq_wait ("netcdf_toRaster", nc.get_taskids())
        print "Completed converting to rasters!"

        # Wait.. Wait... W a i t . . . .
        print "Waiting on Averaging rasters . . ."
        wq.wq_wait(nc.get_tag_name(), nc.get_taskids())
        print "Completed averaging rasters"

        # Wait.. Wait... W a i t . . . .
        print "Waiting on Calculating r.sun . . ."
        wq.wq_wait(r.get_tag_name(), r.get_taskids())
        print "Completed r.sun"

        # Welcome to the (hopefully) the last part of this project
        # EEMT calculations and distribution processes to follow

        taskids = []
        for day in range(1,2):
            command = "python eemt.py %s %s %s %s %s %s %s %s %s" % (demRaster, twiRaster, dem_1km, "tmin", "tmax", "prcp", total_sun, sun_hours, day)
            taskid = wq.wq_job("eemt_toaster", [command, "0", "0"])
            taskids.append(taskid)

        #wait for final eemt task to complete
        print "calculating EEMT"
        wq.wq_wait("eemt_toaster", taskids)

"""
        #and we're kind of done

    # calculate S_i
    # naming schema S_i.(julian_day)


    #dem = "../dems/cali.output.mean.tif"
    #demRaster = "dem_raster"

    """


if __name__ == "__main__":
    main()
