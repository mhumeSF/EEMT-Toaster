import sys, subprocess, re, os
from grid import *


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
    !UNUSED METHOD! This method calls gdalinfo on the object's geotiff file.
    It parses the output to save the center coordinates of the geotiff.
    It outputs a tuple of the lon, lat center coordinates of the geotiff.
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
                    lonlat = coords_list[2]
                    #split them on the comma
                    lon_lat = lonlat.split(',')
                    #if the length of the resulting list is 2
                    if len(lon_lat) == 2:
                        #save lon/lat values
                        lon = lon_lat[0].lower()
                        lat = lon_lat[1][:-1].lower()
                        #append (-)'s for S and W lon/lat values
                        if lat[-1] == 's':
                            lat = '-' + lat[:-1].strip()
                        #remove N,S,E,W letters from strings
                        else:
                            lat = lat[:-1].strip()
                        if lon[-1] == 'w':
                            lon = '-' + lon[:-1].strip()
                        else:
                            lon = lon[:-1].strip()
                        #return the longitude and latitude values as tuple
                        return (lat , lon)
                    else:
                        print("Improper lon/lat format in geotiff file")
                else:
                    print("Improper center coordinate format in geotiff file")
            else:
                print("Could not find center coordinates in gdal output")
        except:
            print("Invalid geotiff file")


    """
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
            
            # This is a static set of lat/longs for testing purposes
            # info = "Upper Left  (  321240.000, 4106000.000) (119d 0'40.18\"W, 37d 4'59.71\"N) \n Lower Right (  526000.000, 2811000.000) ( 80d44'29.28\"W, 25d24'56.39\"N)"
            #search for center coordinates in output of gdalinfo
            UL = re.search('Upper Left(.*)', info)
            LR = re.search('Lower Right(.*)', info)

            # print(UL.group(), LR.group())

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

                    # print (UL, LR)

                    #if the length of the resulting list is 2
                    if len(UL) == 2 and len(LR) == 2:
                        #save lat/lon values in tuple values (lat,lon)
                        ULlon = UL[0].lower().strip()
                        ULlat = UL[1][:-1].lower().strip()
                        LRlon = LR[0].lower().strip()
                        LRlat = LR[1][:-1].lower().strip()

                        #append (-)'s for S and W lon/lat values
                        #remove N,S,E,W letters from strings
                        """
                        if ULlat[-1] == 's':
                            ULlat = '-' + ULlat[:-1]
                        else:
                            ULlat = ULlat[:-1]

                        if ULlon[-1] == 'w':
                            ULlon = '-' + ULlon[:-1]
                        else:
                            ULlon = UL[:-1]

                        #print("changed upper left s's and w's")
                        if LRlat[-1] == 's':
                            LRlat = '-' + LRlat[:-1]
                        else:
                            LRlat = LRlat[:-1]

                        if LRlon[-1] == 'w':
                            LRlon = '-' + LRlon[:-1]
                        else:
                            LRlon = LRlon[:-1]
                        """
                        
                        for coord in [ULlon, ULlat, LRlon, LRlat]:
                            if coord[-1] in ['s', 'w']:
                                coord = '-' + coord[:-1]
                            else:
                                coord = coord[:-1]
                                
                        #print("changed lower rights s's and w's")
                        #return the longitude and latitude values as tuple

                        # print ((ULlat, ULlon), (LRlat, LRlon))

                        return ((ULlat, ULlon), (LRlat, LRlon))

                    else:
                        print("Improper lon/lat format in geotiff file")
                else:
                    print("Improper center coordinate format in geotiff file")
            else:
                print("Could not find center coordinates in gdal output")
        except:
            print("Invalid geotiff file")


    """
    This method converts coordinates in day,hour,minute,second format to
    decimal degrees. It takes one argument, a tuple (lat, lon) for
    the conversion. It returns decimal degree values as (lat, lon)
    """
    def toDegrees(self, coords):
        if coords:
            # prin(coords)
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
                print("No lon/lat values extracted from geotiff, exiting...")
        else:
            print("Improper lat/lon tuple provided as argument to GeoConvert")


    """
    This method generates the os commands necessary to call DaymetR. It takes 
    one argument; a pair of lat/lon coordinates in the form of a tuple.
    The first lat/lon values are the top left corner of the selected region
    and the second two are the bottom left corner of the region. It then
    makes an os call for DaymetR which grabs tiles using the lat lon values.
    """
    def forDaymetR(self, coords, sYear=1980, eYear=2015, param="all", outDir="~/DaymetTiles"):
        if coords:
            #((lat, lon),(lat, lon))
            #parse lat/lon values from input tuples
            print("Coords = " + str(coords))
            UL = coords[0]
            LR = coords[1]
            #generate os command
            command = "Rscript ./Daymet_tiles.R %s %s %d %d %s %s" \
                    % (UL, LR, sYear, eYear, param, outDir)
            #if the output directory doesn't exist, create it
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            """
            command = "Rscript ./Daymet_tiles.R %s %s %s %s %d %d %s %s" \
                    % (ULlat, ULlon, LRlat, LRlon, sYear, eYear, param, outDir)
            """  
            #print(command)   
            try:
                subprocess.check_output(command, shell = True)
            except:
                print("DaymetR command failed, try again!")
        else:
            print("No coordinates supplied for DaymetR")


    """
    This method converts coordinates in decimal lat/lon format into the proper
    format to query the tile number matrix that we have built. It takes one
    argument, a tuple, which is a pair of lat/lon coordinates and returns the
    local matrix indices corresponding to the coords. These can be used to 
    lookup the index of tile IDs.
    """
    def toMatrix(self, coords):
        if coords and len(coords) == 2:
            #get lat/lon coords from arg
            lat = float(coords[0])
            lon = float(coords[1])
            #run the conversion on the lat/lon
            i = abs(int((lat-14)/2))
            j = abs(int((lon+52)/2))
            # print ("converted matrix values: %d %d") % (i,j)
            return (i,j)
        else:
            print("No coordinates specified to convert from decimal to matrix")


    """
    This method takes in (UL LR) as a space-delimited coordinates in a tuple and 
    returns the list of tiles that are contained in this rectangular geographical area.
    """
    def getTiles(self, coords):
        if coords and len(coords) == 2:
            UL = self.toMatrix(coords[0].split())
            LR = self.toMatrix(coords[1].split())
            # if (UL == LR):
            #     return TileIdMatrix[UL[0]][UL[1]]
            # else:
            return self.getTileList ([UL,LR])


    """
    This method takes in 2x(i,j) indices and returns a list of tiles that 
    encompass those indices.
    """
    def getTileList(self, indices):
        i1 = min(indices[0][0], indices[1][0])
        j1 = min(indices[0][1], indices[1][1])
        i2 = max(indices[0][0], indices[1][0])
        j2 = max(indices[0][1], indices[1][1])
 
        # print (i1, j1)
        # print (i2, j2)

        tiles = []

        for i in range(i1, i2 + 1):
            for j in range(j1, j2 + 1):
                tile = TileIdMatrix[i][j]
                if tile > 0 :
                    tiles.append(tile)
        print ("Number of tiles: %d") % len(tiles)
        return tiles


    """
    This method calls gdalwarp on its argument to warp the coordinates of the
    geotiff file to the new coordinate system. It outputs a geotiff file.
    The two arguments are filenames to an input geotiff file and an output
    geotiff file. 
    """ 
    def gdalwarp(self, input, output):
	    command = "gdalwarp -overwrite -s_srs EPSG:26911 -t_srs \
		 \"+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 \
		   +y_0=0 +datum=WGS84 +units=m +no_defs\" -tr 10 10 -r bilinear \
		   -multi -dstnodata 0 -of input output"
	    try:
	        info = subprocess.check_output(command, shell = True)
            return output
	    except:
	        print("Gdalwarp command failed")
