import sys, subprocess, re

#try to get tiff from commnad line args
try:
    tiff = sys.argv[1]
except:
    sys.exit("No geotiff file specified, exiting...")

#generate command for os
command = "gdalinfo " + tiff

#try to run gdalinfo command
try:
    info = subprocess.check_output(command, shell=True)
except:
    sys.exit("Invalid geotiff file, exiting...")

#search for center coordinates in output of gdalinfo
match = re.search('Center(.*)', info)
#old unfinished regex matching
#match = re.search('Center( *)\( ( *)(\d*)\.(\d{3}), (\d*).(\d{3})\)( *)\((\d*)d(\d*)', info)

#if center is found
if match:
    #save match as string
    center_str = match.group()
    #make list of results
    coords_list = center_str.split('(')
    #if the list has 3 elements (assuming proper gdalinfo output format)
    if len(coords_list) == 3:
	longlat = coords_list[2]
	long_lat = longlat.split(',')
	if len(long_lat) == 2: 
	    lat = long_lat[1][:-1].lower()
	    long = long_lat[0].lower()
	    if lat[-1] == 's':
		lat = '-' + lat[:-1].strip()
	    else:
		lat = lat[:-1]
	    if long[-1] == 'w':
		long = '-' + long[:-1].strip()
	    else:
		long = long[:-1]
 	    #print the longitude and latitude values to the screen
	    #print('long = ' + long , 'lat = ' + lat)
	else:
	    sys.exit("Improper lon/lat format in geotiff file, exiting...")
    else:
	sys.exit("Improper center coordinate format in geotiff file, exiting...")
else:
    sys.exit("Could not find center coordinates in gdal output, exiting...")
#add line to convert printed coordinates to UTM and output

#if longitude and latitude values were found
if long and lat:
    #remove white space
    long = re.sub(' ', '', long)
    lat = re.sub(' ', '', lat)
    #generate command for geoconvert
    command = 'echo "' + lat + ' "' + long + ' | GeoConvert -u -p -1'
    #print(command)
    try:
        #run geoconvert to get UTM value
        utm = subprocess.check_output(command, shell=True)
        print(utm.strip())
    except:
	sys.exit("Improper geoconvert command, exiting...")
else:
    sys.exit("No long/lat values extracted from geotiff, exiting...")
