import sys, subprocess, re, os
from grid import *


class geotiff:

    def __init__(self, tiff = None):
        """
        Initializes a new geotiff object.
        Takes one argument, a link to a geotiff file.
        """
        if not tiff:
            tiff = raw_input("Input path to geotiff file: ")
        try:
            self.tiff = tiff
        except:
            print("No valid geotiff file specified, exiting...")


    def getCoordinates(self):
        """
        This method calls gdalinfo on the geotiff file and parses the output to
        acquire the top left and bottom right corner coordinates. The output is
        two tuples, the first being the x,y coordinates of the top left corner
        of the region and the second being the x,y coordinates of the bottom right
        corner of the region.
        """
        #generate command for os
        command = ("gdalinfo " + self.tiff)
        #try to run gdalinfo command
        #info = subprocess.check_output(command, shell = True)
        info = os.popen(command).read()
        # This is a static set of lat/longs for testing purposes
        # info = "Upper Left  (  321240.000, 4106000.000) (119d 0'40.18\"W, 37d 4'59.71\"N) \n Lower Right (  526000.000, 2811000.000) 			( 80d44'29.28\"W, 25d24'56.39\"N)"
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
                    for coord in [ULlon, ULlat, LRlon, LRlat]:
                        if coord[-1] in ['s', 'w']:
                            coord = '-' + coord[:-1]
                        else:
                            coord = coord[:-1]

                    #return the longitude and latitude values as tuple
                    return ((ULlat, ULlon), (LRlat, LRlon))

                else:
                    print("Improper lon/lat format in geotiff file")
            else:
                print("Improper center coordinate format in geotiff file")
        else:
            print("Could not find center coordinates in gdal output")



    def toDegrees(self, coords):
        """
        This method converts coordinates in day,hour,minute,second format to
        decimal degrees. It takes one argument, a tuple (lat, lon) for
        the conversion. It returns decimal degree values as (lat, lon)
        """
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
                    #ULutm = subprocess.check_output(ULcommand, shell=True)
                    #LRutm = subprocess.check_output(LRcommand, shell=True)
                    ULutm = os.popen(ULcommand).read()
                    LRutm = os.popen(LRcommand).read()
                    return (ULutm.strip(), LRutm.strip())
                except:
                    print("Improper geoconvert command, exiting...")
            else:
                print("No lon/lat values extracted from geotiff, exiting...")
        else:
            print("Improper lat/lon tuple provided as argument to GeoConvert")


    def toMatrix(self, coords):
        """
        This method converts coordinates in decimal lat/lon format into the proper
        format to query the tile number matrix that we have built. It takes one
        argument, a tuple, which is a pair of lat/lon coordinates and returns the
        local matrix indices corresponding to the coords. These can be used to
        lookup the index of tile IDs.
        """
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


    def getTiles(self, coords):
        """
        This method takes in (UL LR) as a tuple and returns the list of tiles
        that are contained in this rectangular geographical area.
        """
        #if two command line arguments are specified
        if coords and len(coords) == 2:
	    #parse them as a pair of lat/long values coresponding to the
	    #upper left and lower right of the region
	    #then convert the format to matrix indices
            UL = self.toMatrix(coords[0].split())
            LR = self.toMatrix(coords[1].split())

	#save the matrix indices individually, 0's are lats, 1's are longs
        i1 = min(UL[0], LR[0])
        j1 = min(UL[1], LR[1])
        i2 = max(UL[0], LR[0])
        j2 = max(UL[1], LR[1])

	#create empty list for tile IDs to go
        tiles = []

	#iterate through all i-indices
        for i in range(i1, i2 + 1):
	    #iterate through all j-indices
            for j in range(j1, j2 + 1):
		#get the tile ID for that i,j index and append it to the list
                tile = TileIdMatrix[i][j]
                if tile > 0 :
                    tiles.append(tile)
	#return the list of tiles
        print ("Number of tiles: %d") % len(tiles)
        return tiles


    def gdalwarp(self, input, output):
        """
        This method calls gdalwarp on its argument to warp the coordinates of the
        geotiff file to the new coordinate system. It outputs a geotiff file.
        The two arguments are filenames to an input geotiff file and an output
        geotiff file.
        """
        command = "gdalwarp -overwrite -s_srs EPSG:26911 -t_srs \
                \"+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 \
                +y_0=0 +datum=WGS84 +units=m +no_defs\" -tr 10 10 -r bilinear \
                -multi -dstnodata 0 -of input output"
        try:
            info = subprocess.check_output(command, shell = True)
            return output
        except:
            print("Gdalwarp command failed")
