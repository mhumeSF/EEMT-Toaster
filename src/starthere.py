#!/usr/bin/python2

import sys, os, subprocess
from netcdf import *
from geotiff import *
from raster import *
from datetime import date

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
        print ("Usage: %s <list_of_years> <list_of_param(s)> <list_of_tiff_file(s)>") % sys.argv[0]
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

    for tiff in tiff_files:
        print ("Processing: " + tiff)
        locn = geotiff(tiff)
        coords = locn.getCoordinates()
        degrees = locn.toDegrees(coords)
        tile_list = locn.getTiles (degrees)
        print tile_list

        for param in params_to_use:
            for year in years:
                cdffile = netcdf(year, tile_list, param)
                netcdfs.append(cdffile)

if __name__ == "__main__":
    main()
