#!/usr/bin/python2

import system, os
from raster import *
from geotiff import *
from netcdf import *

#eemt.py [dem_10m] [dem_TWI] [year]

#************************************************************#
# needs total_sun and sun_hours ... inputs from outside!!!!! #
#************************************************************#

#na_dem
command = "r.in.gdal input=../../na_dem.tif output=na_dem"
dem_1k = "na_dem"

#setup 10m raster warp it etc etc
dem_10m = "dem_10m"
TWI = "TWI"
r = raster(sys.argv[1], dem_10m)
r2 = raster(system.argv[2], TWI)

year = int(sys.argv[3])

tminRaster = netcdf(year, tiles, "tmin")
tmaxRaster = netcdf(year, tiles, "tmax")
prcpRaster = netcdf(year, tiles, "prcp")

c_w = "c_w"
command = "r.mapcalc \"4185.5\""

h_bio = "h_bio"
command = "r.mapcalc \"22*10^6\""

a_i = "a_i." + str(i)
command = "r.mapcalc \"%s=%s/((max(%s)+min(%s))/2)\"" % (a_i,TWI,TWI,TWI)

for i in range(1,366):
    
    
    #************************************************************#
    # tmin_loc                                                   #
    #************************************************************#
    tmin = tminRaster + "." + str(i)
    tmin_loc = tminRaster + "_loc." + str(i)
    command = "r.mapcalc \"%s=%s-0.00649*(%s-%s)\"" % (tmin_loc,tmin,dem_10m,dem_1km)
    
    #************************************************************#
    # tmax_loc                                                   #
    #************************************************************#
    tmax = tmaxRaster + "." + str(i)
    tmax_loc = tmaxRaster + "_loc." + str(i)
    command = "r.mapcalc \"%s=%s-0.00649*(%s-%s)\"" % (tmax_loc,tmax,dem_10m,dem_1km)
    
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
    S_i = "S_i." + str(i)
    command = "r.mapcalc \"%s=%s/%s\"" % (S_i, total_sun, flat_total_sun)
    
    tmin_topo = "tmin_topo." + str(i)
    command = "r.mapcalc \"%s=%s+(%s-(1/%s))\"" % (tmin_topo, tmin_loc,S_i,S_i)
    
    tmax_topo = "tmax_topo." + str(i)
    command = "r.mapcalc \"%s=%s+(%s-(1/%s))\"" % (tmax_topo, tmax_loc,S_i,S_i)
    
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
    
    m_vp = "m_vp." str(i)
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
    
    F = "F." + str(i)
    command = "r.mapcalc \"%s=%s*%s\"" % (F, a_i, prcp)
    
    NPP_trad = "NPP_trad." + str(i)
    command = "r.mapcalc \"%s=3000*(1+exp(1.315-0.119*(%s+%s)/2)^-1)\"" % (NPP_trad, tmax_loc, tmin_loc)
    
    E_bio = "E_bio." + str(i)
    command = "r.mapcalc \"%s=%s*(22*10^6)\"" % (E_bio, NPP_trad)
    
    E_ppt = "E_ppt." + str(i)
    command = "r.mapcalc \"%s=%s*4185.5*%s*%s\"" % (E_ppt, F, DT, E_bio)
    
    EEMT-TOPO = "EEMT-TOPO." + str(i)
    command = "r.mapcalc \"%s=%s+%s\"" % (EEMT-TOPO, E_ppt, E_bio)
    
    
    
    
    
    
    


