import sys, subprocess, re, os
TileIdMatrix = [
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 9405, 9404, 9403, 9402, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 9587, 9586, 9585, 9584, 9583, 9582, 9581, 9580, 9579, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 9767, 9766, 9765, 9764, 9763, 9762, 9761, 9760, 9759, 9758, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 9947, 9946, 9945, 00000, 00000, 9942, 9941, 9940, 9939, 9938, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 10122, 10121, 10120, 10119, 10118, 10117, 10116, 10115, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 10310, 10309, 00000, 00000, 00000, 00000, 00000, 00000, 10302, 10301, 10300, 10299, 10298, 10297, 10296, 10295, 10294, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 10490, 10489, 00000, 00000, 00000, 00000, 00000, 00000, 10482, 10481, 10480, 10479, 10478, 10477, 10476, 10475, 10474, 10473, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 10670, 10669, 10668, 00000, 10666, 10665, 10664, 10663, 10662, 10661, 10660, 10659, 10658, 10657, 10656, 10655, 10654, 10653, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 10850, 10849, 10848, 10847, 10846, 10845, 10844, 10843, 10842, 10841, 10840, 10839, 10838, 10837, 10836, 10835, 10834, 10833, 10832, 00000, 00000, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 11032, 11031, 11030, 11029, 11028, 11027, 11026, 11025, 11024, 11023, 11022, 11021, 11020, 11019, 11018, 11017, 11016, 11015, 11014, 11013, 11012, 11011, 11010, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 11213, 11212, 11211, 11210, 11209, 11208, 11207, 11206, 11205, 11204, 11203, 11202, 11201, 11200, 11199, 11198, 11197, 11196, 11195, 11194, 11193, 11192, 11191, 11190, 00000, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 11392, 11391, 11390, 11389, 11388, 11387, 11386, 11385, 11384, 11383, 11382, 11381, 11380, 11379, 11378, 11377, 11376, 11375, 11374, 11373, 11372, 11371, 11370, 11369, 00000, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 11573, 11572, 11571, 11570, 11569, 11568, 11567, 11566, 11565, 11564, 11563, 11562, 11561, 11560, 11559, 11558, 11557, 11556, 11555, 11554, 11553, 11552, 11551, 11550, 11549, 11548, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 11756, 11755, 11754, 11753, 11752, 11751, 11750, 11749, 11748, 11747, 11746, 11745, 11744, 11743, 11742, 11741, 11740, 11739, 11738, 11737, 11736, 11735, 11734, 11733, 11732, 11731, 11730, 11729, 11728, 00000, 00000, 00000],
        [00000, 00000, 00000, 00000, 00000, 00000, 11938, 11937, 11936, 11935, 11934, 11933, 11932, 11931, 11930, 11929, 11928, 11927, 11926, 11925, 11924, 11923, 11922, 11921, 11920, 11919, 11918, 11917, 11916, 11915, 11914, 11913, 11912, 11911, 11910, 11909, 11908, 00000, 00000, 00000],
        [00000, 00000, 00000, 12121, 12120, 12119, 12118, 12117, 12116, 12115, 12114, 12113, 12112, 12111, 12110, 12109, 12108, 12107, 12106, 12105, 12104, 12103, 12102, 12101, 12100, 12099, 12098, 12097, 12096, 12095, 12094, 12093, 12092, 12091, 12090, 12089, 12088, 00000, 00000, 00000],
        [12304, 12303, 12302, 12301, 12300, 12299, 12298, 12297, 12296, 12295, 12294, 12293, 12292, 12291, 12290, 12289, 12288, 12287, 12286, 12285, 12284, 12283, 12282, 12281, 12280, 12279, 12278, 12277, 12276, 12275, 12274, 12273, 12272, 12271, 12270, 12269, 12268, 00000, 00000, 00000],
        [12484, 12483, 12482, 12481, 12480, 12479, 12478, 12477, 12476, 12475, 12474, 12473, 12472, 12471, 12470, 12469, 12468, 12467, 12466, 12465, 12464, 12463, 12462, 12461, 12460, 12459, 12458, 12457, 12456, 12455, 12454, 12453, 12452, 12451, 12450, 12449, 12448, 12447, 00000, 00000],
        [00000, 12663, 12662, 12661, 12660, 12659, 12658, 12657, 12656, 12655, 12654, 12653, 12652, 12651, 12650, 12649, 12648, 12647, 12646, 12645, 12644, 12643, 12642, 12641, 12640, 12639, 12638, 12637, 12636, 12635, 12634, 12633, 12632, 12631, 12630, 12629, 12628, 12627, 12626, 12625],
        ]

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

            # print (UL.group(), LR.group())

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
            # print (coords)
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
    def getTiles (self, coords):
        if coords and len(coords) == 2:
            UL = self.toMatrix(coords[0].split())
            LR = self.toMatrix(coords[1].split())
            # if (UL == LR):
            #     return TileIdMatrix[UL[0]][UL[1]]
            # else:
            return self.getTileList ([UL,LR])

    """
    This method takes in 2x(i,j) indices and returns a list of tiles
    """
    def getTileList (self, indices):
        i1 = min (indices[0][0], indices[1][0])
        j1 = min (indices[0][1], indices[1][1])
        i2 = max (indices[0][0], indices[1][0])
        j2 = max (indices[0][1], indices[1][1])
 
        # print (i1, j1)
        # print (i2, j2)

        tiles = []

        for i in range (i1, i2 + 1):
            for j in range (j1, j2 + 1):
                tile = TileIdMatrix[i][j]
                if tile > 0 :
                    tiles.append(tile)
        print ("Number of tiles: %d") % len(tiles)
        return tiles

    def gdalwarp(self, something):
        return

