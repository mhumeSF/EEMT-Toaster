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
    This method converts coordinates in day,hour,minute,second format to
    decimal degrees. It takes one argument, a tuple (lat, long) for
    the conversion. It returns decimal degree values as (lat, long)
    """
    def toDegrees(self, center):
        if center:
            #if longitude and latitude values were found
            if len(center) == 2:
                long = center[1]
                lat = center[0]
                #remove white space
                long = re.sub(' ', '', long)
                lat = re.sub(' ', '', lat)
                #generate command for geoconvert (command outputs UTM format)
                command = 'echo "' + lat + ' "' + long + ' | GeoConvert -g -p -1'
                #print(command) #for debugging
                try:
                    #run geoconvert to get UTM value
                    utm = subprocess.check_output(command, shell=True)
                    return utm.strip()
                except:
                    print("Improper geoconvert command, exiting...")
            else:
                print("No long/lat values extracted from geotiff, exiting...")
        else:
            print("Improper lat/long tuple provided as argument to GeoConvert")


#def gdalwarp(self):
