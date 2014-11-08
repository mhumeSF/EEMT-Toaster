import sys, subprocess, re, os

class geotiff:

    """
    Initializes a new geotiff object.
    Takes one argument, a link to a geotiff file.
    """
    def __init__(self, tiff = None):
        if not tiff:
           tiff = raw_input("Input path to geotiff file: ")
        try:
            self.tiff = tiff
        except:
            print("No valid geotiff file specified, exiting...")

    """
    This method calls gdalinfo on the object's geotiff file.  It parses the 
    output to save the center coordinates of the geotiff. It outputs a tuple 
    of the lon, lat center coordinates of the geotiff.  
    """
    def getCenter(self):
        #generate command for os
        command = ("gdalinfo " + self.tiff)
        #try to run gdalinfo command
        try:
            info = subprocess.check_output(command, shell = True)
            #search for center coordinates in output of gdalinfo
            match = re.search('Center(.*)', info)

            #if center is found
            if match:
                #save match as string
                center_str = match.group()
                #make list of results
                coords_list = center_str.split('(')
                #if the list has 3 elements (assuming proper gdalinfo output format)
                if len(coords_list) == 3:
                    #save Center values(assumed to be 3rd item)
                    longlat = coords_list[2]
                    #split them on the comma
                    long_lat = longlat.split(',')
                    #if the length of the resulting list is 2
                    if len(long_lat) == 2:
                        #save long/lat values
                        long = long_lat[0].lower()
                        lat = long_lat[1][:-1].lower()
                        #append (-)'s for S and W long/lat values
                        if lat[-1] == 's':
                            lat = '-' + lat[:-1].strip()
                        #remove N,S,E,W letters from strings
                        else:
                            lat = lat[:-1]
                        if long[-1] == 'w':
                            long = '-' + long[:-1].strip()
                        else:
                            long = long[:-1]
                        #return the longitude and latitude values as tuple
                        return (lat , long)
                    else:
                        print("Improper long/lat format in geotiff file")
                else:
                    print("Improper center coordinate format in geotiff file")
            else:
                print("Could not find center coordinates in gdal output")
        except:
            print("Invalid geotiff file")


    """
<<<<<<< HEAD
    This method calls gdalinfo on the geotiff file and parses the output to
    acquire the top left and bottom right corner coordinates. The output is
    two tuples, the first being the x,y coordinates of the top left corner
    of the region and the second being the x,y coordinates of the bottom right
    corner of the region.
    """
    def getCoordinates(self):
        #generate command for os
        command = ("gdalinfo " + self.tiff)
        #try to run gdalinfo command
        try:
            info = subprocess.check_output(command, shell = True)

            #search for center coordinates in output of gdalinfo
            UL = re.search('Upper Left(.*)', info)
            LR = re.search('Lower Right(.*)', info)

            #if center is found
            if UL and LR:
                #save match as string
                UL_str = UL.group()
                LR_str = LR.group()
                #make list of results
                UL = UL_str.split('(')
                LR = LR_str.split('(')
                #if the list has 3 elements (assuming proper gdalinfo output format)
                if len(UL) == 3 and len(LR) == 3:
                    #save coordinate values(assumed to be 3rd item)
                    UL = UL[2]
                    LR = LR[2]
                    #split them on the comma
                    UL = UL.split(',')
                    LR = LR.split(',')
                    #if the length of the resulting list is 2
                    if len(UL) == 2 and len(LR) == 2:
                        #save lat/long values in tuple values (lat,long)
                        ULlong = UL[0].lower().strip()
                        ULlat = UL[1][:-1].lower().strip()
                        LRlong = LR[0].lower().strip()
                        LRlat = LR[1][:-1].lower().strip()

                        #append (-)'s for S and W long/lat values
                        #remove N,S,E,W letters from strings
                        if ULlat[-1] == 's':
                            ULlat = '-' + ULlat[:-1]
                        else:
                            ULlat = ULlat[:-1]

                        if ULlong[-1] == 'w':
                            ULlong = '-' + ULlong[:-1]
                        else:
                            ULlong = UL[:-1]

                        #print("changed upper left s's and w's")
                        if LRlat[-1] == 's':
                            LRlat = '-' + LRlat[:-1]
                        else:
                            LRlat = LRlat[:-1]

                        if LRlong[-1] == 'w':
                            LRlong = '-' + LRlong[:-1]
                        else:
                            LRlong = LRlong[:-1]

                        #print("changed lower rights s's and w's")
                        #return the longitude and latitude values as tuple
                        return ((ULlat, ULlong), (LRlat, LRlong))

                    else:
                        print("Improper long/lat format in geotiff file")
                else:
                    print("Improper center coordinate format in geotiff file")
            else:
                print("Could not find center coordinates in gdal output")
        except:
            print("Invalid geotiff file")


    """
    This method converts coordinates in day,hour,minute,second format to
    decimal degrees. It takes one argument, a tuple (lat, long) for
    the conversion. It returns decimal degree values as (lat, long)
    """
    def toDegrees(self, coords):
        if coords:
            if len(coords) == 2:
                #if longitude and latitude values were found
                UL = coords[0]
                LR = coords[1]
                #remove white space
                UL = (re.sub(' ', '', UL[0]), re.sub(' ', '', UL[1]))
                LR = (re.sub(' ', '', LR[0]), re.sub(' ', '', LR[1]))
                #generate command for geoconvert (command outputs UTM format)
                ULcommand = 'echo "' + UL[0] + ' "' + UL[1] + ' | GeoConvert -g -p -1'
                LRcommand = 'echo "' + LR[0] + ' "' + LR[1] + ' | GeoConvert -g -p -1'
                #print(command) #for debugging
                try:
                    #run geoconvert to get UTM value
                    ULutm = subprocess.check_output(ULcommand, shell=True)
                    LRutm = subprocess.check_output(LRcommand, shell=True)
                    return (ULutm.strip(), LRutm.strip())
                except:
                    print("Improper geoconvert command, exiting...")
            else:
                print("No long/lat values extracted from geotiff, exiting...")
        else:
            print("Improper lat/long tuple provided as argument to GeoConvert")

    """
    This method generates the os commands necessary to call DaymetR. It takes 
    one argument; a pair of lat/long coordinates in the form of a tuple.
    The first lat/long values are the top left corner of the selected region
    and the second two are the bottom left corner of the region. It then
    makes an os call for DaymetR which grabs tiles using the lat long values.
    """
    def forDaymetR(self, coords, sYear=1980, eYear=2015, param="all", outDir="~/DaymetTiles"):
        if coords:
            #((lat, long),(lat, long))
            #parse lat/long values from input tuples
            print("Coords = " + str(coords))
            UL = coords[0]
            LR = coords[1]
            #generate os command
            command = "Rscript ./Daymet_tiles.R %s %s %d %d %s %s" \
                % (UL, LR, sYear, eYear, param, outDir)
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            """
            command = "Rscript ./Daymet_tiles.R %s %s %s %s %d %d %s %s" \
                % (ULlat, ULlong, LRlat, LRlong, sYear, eYear, param, outDir)

            """  
            #print(command)   
            try:
                subprocess.check_output(command, shell = True)
            except:
                print("DaymetR command failed, try again!")
            
        else:
            print("No coordinates supplied for DaymetR")


    def gdalwarp(self, something):
        return

