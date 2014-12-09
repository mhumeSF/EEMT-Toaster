#!/usr/bin/python2

import os
from raster import *
from geotiff import *
from netcdf import *

#eemt.py [dem_10m] [dem_TWI] [year]

#************************************************************#
# needs total_sun and sun_hours ... inputs from outside!!!!! #
#************************************************************#

'''
so far I have this setup to calculate EEMT-TOPO only.  Some of the calculatons for Trad
are in there, however, I don't think the information Tyson put up on the website is
complete.  I need more information, but this will have to suffice until then.

I need a way to get total_sun and sun_hours from outside into this script.
total_sun = glob_rad
sun_hours = insol_time

Also, another nice thing to see in this would be a way to parallelize everything within
the for loop.  I know it can be done, I just don't yet know how Sri got work_queue working.
perhaps this is something we can work out the next time we meet up.

The three inputs to this script are the OpenTopo Dem, a total wetness index dem also from Open
Topo and the year.  We could include options for montly averages in a later version, but I
would like to see this working before I go there.
'''

if len(sys.argv) < 3:
    print "not enough arguments\n"
    print "usage [dem_10m] [dem_TWI] [year]"
    exit(1)

#na_dem
command = "r.in.gdal input=../../na_dem.tif output=na_dem"
dem_1k = "na_dem"

#setup 10m raster warp it etc etc
dem_10m = "dem_10m"
TWI = "TWI"

dem_10m_tiff = sys.argv[1]
twi_tiff = sys.argv[2]

r = raster(dem_10m_tiff, dem_10m)
r2 = raster(twi_tiff, TWI)

year = int(sys.argv[3])

total_sun = "glob"
sun_hours = "insol"

locn = geotiff(dem_10m_tiff)
coords = locn.getCoordinates()
degrees = locn.toDegrees(coords)
tiles = locn.getTiles(degrees)

#debug
print tiles

tminRaster = netcdf(year, tiles, "tmin")
tmaxRaster = netcdf(year, tiles, "tmax")
prcpRaster = netcdf(year, tiles, "prcp")

tminRaster = tminRaster.patchRaster
tmaxRaster = tmaxRaster.patchRaster
prcpRaster = prcpRaster.patchRaster

print tminRaster
print tmaxRaster
print prcpRaster

#c_w = "c_w"
#command = "r.mapcalc \"4185.5\""
#os.system(command)
c_w = 4185.5

#h_bio = "h_bio"
#command = "r.mapcalc \"22*10^6\""
#os.system(command)
h_bio = 22**10^6

a_i = "a_i"
command = "r.mapcalc \"%s=%s/((max(%s)+min(%s))/2)\"" % (a_i,TWI,TWI,TWI)
os.system(command)

for i in range(1,366):
    
    
    #************************************************************#
    # tmin_loc                                                   #
    #************************************************************#
    tmin = tminRaster + "." + str(i)
    tmin_loc = tminRaster + "_loc." + str(i)
    command = "r.mapcalc \"%s=%s-0.00649*(%s-%s)\"" % (tmin_loc,tmin,dem_10m,dem_1km)
    os.system(command)

    #************************************************************#
    # tmax_loc                                                   #
    #************************************************************#
    tmax = tmaxRaster + "." + str(i)
    tmax_loc = tmaxRaster + "_loc." + str(i)
    command = "r.mapcalc \"%s=%s-0.00649*(%s-%s)\"" % (tmax_loc,tmax,dem_10m,dem_1km)
    os.system(command)
    
    #************************************************************#
    # LOCAL_PET                                                  #
    #************************************************************#
    f_tmin_loc = "f_" + tmin_loc
    command = "r.mapcalc \"%s=6.108*exp((17.27*%s)/(%s+273.3))\"" % (f_tmin_loc, tmin_loc, tmin_loc)

    f_tmax_loc = "f_" + tmax_loc
    command = "r.mapcalc \"%s=6.108*exp((17.27*%s)/(%s+273.3))\"" % (f_tmax_loc, tmax_loc, tmax_loc)
    
    vp_s = "vp_s." + str(i)
    command = "r.mapcalc \"%s=(%s+%s)/2\"" % (vp_s, f_tmax_loc, f_tmin_loc)
    
    LOCAL_PET = "LOCAL_PET." + str(i)
    command = "r.mapcalc \"%s=(2.1*((%s/12)^2)*%s/((%s+%s)/2)\"" % (LOCAL_PET, hours_sun, vp_s, tmax_loc, tmin_loc)
    
    #************************************************************#
    # Locally corrected temperature that account for s_i         #
    #************************************************************#

    
    total_sun = "glob_" + str(i)
    sun_hours = "insol_" + str(i)
    
    zeros = "zeros." + str(i)
    command = "r.mapcalc \"%s=if(%s>0,0,null())\"" % (zeros, dem_10m)
    os.system(command)

    flat_total_sun = "glob_rad_flat." + str(i)
    command = "r.sun elevin=%s aspin=%s slipein=%s day=\"" + str(i) + "\" step=\".05\" dist=\"1\" glob_rad=%s" % (dem_10m, zeros, zeros, flat_total_sun)
    os.system(command)

    S_i = "S_i." + str(i)
    command = "r.mapcalc \"%s=%s/%s\"" % (S_i, total_sun, flat_total_sun)
    os.system(command)
    
    tmin_topo = "tmin_topo." + str(i)
    command = "r.mapcalc \"%s=%s+(%s-(1/%s))\"" % (tmin_topo, tmin_loc,S_i,S_i)
    os.system(command)    

    tmax_topo = "tmax_topo." + str(i)
    command = "r.mapcalc \"%s=%s+(%s-(1/%s))\"" % (tmax_topo, tmax_loc,S_i,S_i)
    os.system(command)    

    #************************************************************#
    # Water Balance                                              #
    #************************************************************#  
   
    
    #************************************************************#
    # PET                                                        #
    #************************************************************#
    total_sun_joules = "total_sun_joules." + str(i)
    command = "r.mapcalc \"%s=%s*3600\"" % (total_sun_joules, total_sun)
    
    p_a = "p_a." + str(i)
    command = "r.mapcalc \"101325*exp(-9.80665*0.289644*%s/(8.31447*288.15))/287.35*((%s+%s/2)+273.125) % (dem_10m, tmax_topo, tmin_topo)\""
    
    f_tmin_topo = "f_tmin_topo." + str(i)
    command = "r.mapcalc \"%s=6.108*exp((17.27*%s)/(%s+237.3))\"" % (f_tmin_topo, tmin_topo, tmin_topo)
    
    f_tmax_topo = "f_tmax_topo." + str(i)
    command = "r.mapcalc \"%s=6.108*exp((17.27*%s)/(%s+237.3))\"" % (f_tmax_topo, tmax_topo, tmax_topo)
    
    vp_s_topo = "vp_s_topo." + str(i)
    command = "r.mapcalc \"%s=(%s+%s)/2\"" % (vp_s_topo, f_tmax_topo, f_tmin_topo)
    
    vp_loc = "vp_loc." + str(i)
    command = "r.mapcalc \"%s=6.11*10^(7.5*%s)/(237.3+%s)\"" % (vp_loc,tmin_topo, tmin_topo)
    
    ra = "ra." + str(i)
    command = "r.mapcalc \"%s=(4.72*(ln(2/0.00137))^2)/(1+0.536*5)\"" % (ra)
    
    m_vp = "m_vp." + str(i)
    command = "r.mapcalc \"%s=0.04145*exp(0.06088*(%s+%s/2))\"" % (m_vp, tmax_topo, tmin_topo)
    
    g_psy = "g_psy." + str(i)
    command = "r.mapcalc \"%s=0.001013*(101.3*((293-0.00649*%s)/293)^5.26)/(0.622*2.45)\"" % (g_psy, dem_10m)
    
    PET = "PET." + str(i)
    command = "r.mapcalc \"%s=%s+%s*0.001013*(%s-%s)/%s))/(2.45*(%s+%s))\"" % (total_sun_joules,p_a,vp_s_topo,vp_loc,ra,m_vp,g_psy)
    
    prcp = prcpRaster + "." + str(i)
    AET = "AET." + str(i)
    command = "r.mapcalc \"%s=%s*(1+%s/%s-(1+(%s/%s)^2.63)^(1/2.63))\"" (AET,prcp, PET, prcp, PET, prcp)
    
    #************************************************************#
    # EEMT-TOPO                                                  #
    #************************************************************#
    
    DT = "DT." + str(i)
    command = "r.mapcalc \"%s((%s+%s)/2) - 273.15\"" % (DT, tmax_topo, tmin_topo)
    os.system(command)    
  
    F = "F." + str(i)
    command = "r.mapcalc \"%s=%s*%s\"" % (F, a_i, prcp)
    os.system(command)    

    NPP_trad = "NPP_trad." + str(i)
    command = "r.mapcalc \"%s=3000*(1+exp(1.315-0.119*(%s+%s)/2)^-1)\"" % (NPP_trad, tmax_loc, tmin_loc)
    os.system(command)    

    E_bio = "E_bio." + str(i)
    command = "r.mapcalc \"%s=%s*(22*10^6)\"" % (E_bio, NPP_trad)
    os.system(command)    

    E_ppt = "E_ppt." + str(i)
    command = "r.mapcalc \"%s=%s*4185.5*%s*%s\"" % (E_ppt, F, DT, E_bio)
    os.system(command)    

    EEMT_TOPO = "EEMT-TOPO." + str(i)
    command = "r.mapcalc \"%s=%s+%s\"" % (EEMT_TOPO, E_ppt, E_bio)
    os.system(command)      

