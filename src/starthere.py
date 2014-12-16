#!/usr/bin/python2

import sys, os, subprocess
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
    # if no args, suicide
    if len(sys.argv) == 1:
        print ("Usage: %s <list_of_years> <list_of_param(s)> <list_of_tiff_file(s)> <TWI:twi tiff to use>") % sys.argv[0]
        sys.exit("Command Line Args")

    # these are the only params that will be accepted
    possible_params = ["dayl", "prcp", "srad", "tmin", "tmax", "vp", "swe"]

    # initialize empty lists each for year, params and tiff files gathered from user input
    params_to_use = []
    tiff_files = []
    years = []

    # Now, the dirty drill!! PARSE!!
    for i in sys.argv[1:]:
        # If it is a param, add it, else...
        if i in possible_params:
            params_to_use.append(i)
        # If it is a valid tiff file
        elif is_tiff_file (i):
            tiff_files.append(i)
        elif "TWI" in i[:3] and is_tiff_file (i[4:]):
            twi_file = i[4:]
        elif "1KM" in i[:3]:
            dem_1km = i[4:]

        # if nothing else, check if it is a valid year after 1980 till year before current
        else:
            try:
                year = int(i)
                if year in range(1980, date.today().year):
                    years.append(year)
            except:
                print ("Discarding meaningless argument: " + i)

    print years
    print params_to_use
    print tiff_files

    if len(params_to_use) == 0:
        params_to_use = possible_params

    netcdfs = []
    wq = workQ()
    nc = netcdf(wq)


    for tiff in tiff_files:
        print ("Processing: " + tiff)
        locn = geotiff(tiff)
        coords = locn.getCoordinates()
        degrees = locn.toDegrees(coords)
        tile_list = locn.getTiles (degrees)
        print tile_list

        twiRaster = "twiRaster"
        twi_r = raster(twi_file, twiRaster, wq)
        
        demRaster = "demRaster"
        r = raster(tiff, demRaster, wq)
        slope = "slope"
        aspect = "aspect"
        r.slopeAspect(demRaster, slope, aspect)

        myStep = "0.05"

        sun_hours = "sun_hours"
        total_sun = "total_sun"

        for day in range(1,366):
            insol_time = sun_hours + "." + str(day)
            glob_rad = total_sun + "." + str(day)
            r.sun(demRaster, slope, aspect, str(day), myStep, insol_time, glob_rad)

        
        for param in params_to_use:
            netcdfs.append(nc.process(years, tile_list, param))
        
        print "Downloading files:"
        wq.wq_wait(nc.get_tag_name(), nc.get_taskids())

        nc.averageRasters() # cues up more jobs in the nc object -> another wait must be executed
        
        print "Averaging rasters:"
        wq.wq_wait(nc.get_tag_name(), nc.get_taskids())

        print "Calculating r.sun:"
        wq.wq_wait(r.get_tag_name(), r.get_taskids())

        taskids = []
        for day in range(1,366):
            command = "python eemt.py %s %s %s %s %s %s %s %s %s" % (demRaster, twiRaster, dem_1km, "tmin", "tmax", "prcp", total_sun, sun_hours, day)
            taskid = wq.wq_job("eemt_toaster", [command, "0", "0"]) 
            taskids.append(taskid)

        #wait for final eemt task to complete
        print "calculating EEMT"
        wq.wq_wait("eemt_toaster", taskids)

        #and we're kind of done

    # calculate S_i
    # naming schema S_i.(julian_day)


    #dem = "../dems/cali.output.mean.tif"
    #demRaster = "dem_raster"



if __name__ == "__main__":
    main()
