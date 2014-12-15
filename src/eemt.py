#!/usr/bin/python2

import os
from raster import *
from geotiff import *

#****************************************************************************#
# Inputs:
# dem_10m the elevation dem from openTopo
# dem_TWI the TWI dem either calculated or gathered from OpenTopo
# na_dem: the 1 km dem from daymet
# tminRaster: the raster with tmin data for each day of an average year
# tmaxRaster: the raster with tmax data for each day of an average year
# prcpRaster: the raster with prcp data for each day of an average year
# S_i: the total_sun to flat_total_sun ratio computed earlier
# total_sun: the set of rasters with glob_rad for each day
# sun_hours: the set of rasters with insol_time for each day
# day: the day of the year to work on
#****************************************************************************#

#*************************************************************#
# All output variables output as a raster                     #
#*************************************************************#
#
# a_i = "a_i" + str(i)
# tmin = tminRaster + "." + str(i)
# tmin_loc = tminRaster + "_loc." + str(i)
# tmax = tmaxRaster + "." + str(i)
# tmax_loc = tmaxRaster + "_loc." + str(i)
# f_tmin_loc = "f_" + tmin_loc
# f_tmax_loc = "f_" + tmax_loc
# vp_s = "vp_s." + str(i)
# LOCAL_PET = "LOCAL_PET." + str(i)
# S_i = S_i + "." + str(i)
# tmin_topo = "tmin_topo." + str(i)
# total_sun_joules = "total_sun_joules." + str(i)
# p_a = "p_a." + str(i)
# f_tmin_topo = "f_tmin_topo." + str(i)
# f_tmax_topo = "f_tmax_topo." + str(i)
# vp_s_topo = "vp_s_topo." + str(i)
# vp_loc = "vp_loc." + str(i)
# ra = "ra." + str(i)
# m_vp = "m_vp." + str(i)
# g_psy = "g_psy." + str(i)
# PET = "PET." + str(i)
# prcp = prcpRaster + "." + str(i)
# AET = "AET." + str(i)
# DT = "DT." + str(i)
# F = "F." + str(i)
# NPP_trad = "NPP_trad." + str(i)
# E_bio = "E_bio." + str(i)
# E_ppt = "E_ppt." + str(i)
# EEMT_TOPO = "EEMT_TOPO." + str(i)
#
#*************************************************************#


if len(sys.argv) < 3:
    print "not enough arguments\n"
    print "usage [dem_10m] [dem_TWI] [na_dem] [tminRaster] [tmaxRaster] [prcpRaster] [S_i] [total_sun] [sun_hours] [day]"
    exit(1)

#na_dem
na_dem = sys.argv[3]
dem_1km = "na_dem"
command = "r.external input=" + na_dem + " output=" + dem_1km + " --overwrite"
os.system(command)

#setup 10m raster warp it etc etc
dem_10m = "dem_10m"
TWI = "TWI"

dem_10m_tiff = sys.argv[1]
twi_tiff = sys.argv[2]

r = raster(dem_10m_tiff, dem_10m)
r2 = raster(twi_tiff, TWI)

S_i = sys.argv[7]
total_sun = sys.argv[8]
sun_hours = sys.argv[9]
i = sys.argv[10] # day of the year

tminRaster = sys.argv[4]
tmaxRaster = sys.argv[5]
prcpRaster = sys.argv[6]

c_w = 4185.5

h_bio = 22**10^6



a_i = "a_i"
command = "r.mapcalc \"%s=%s/((max(%s)+min(%s))/2)\"" % (a_i,TWI,TWI,TWI)
print command
os.system(command)

#************************************************************# 
# tmin_loc                                                   #
#************************************************************#
tmin = tminRaster + "." + str(i)
tmin_loc = tminRaster + "_loc." + str(i)
command = "r.mapcalc \"%s=%s-0.00649*(%s-%s)\"" % (tmin_loc,tmin,dem_10m,dem_1km)
print command
os.system(command)

#************************************************************#
# tmax_loc                                                   #
#************************************************************#
tmax = tmaxRaster + "." + str(i)
tmax_loc = tmaxRaster + "_loc." + str(i)
command = "r.mapcalc \"%s=%s-0.00649*(%s-%s)\"" % (tmax_loc,tmax,dem_10m,dem_1km)
print command
os.system(command)

#************************************************************#
# LOCAL_PET                                                  #
#************************************************************#
f_tmin_loc = "f_" + tmin_loc
command = "r.mapcalc \"%s=6.108*exp((17.27*%s)/(%s+273.3))\"" % (f_tmin_loc, tmin_loc, tmin_loc)
print command
os.system(command)

f_tmax_loc = "f_" + tmax_loc
command = "r.mapcalc \"%s=6.108*exp((17.27*%s)/(%s+273.3))\"" % (f_tmax_loc, tmax_loc, tmax_loc)
print command
os.system(command)

vp_s = "vp_s." + str(i)
command = "r.mapcalc \"%s=(%s+%s)/2\"" % (vp_s, f_tmax_loc, f_tmin_loc)
print command
os.system(command)

LOCAL_PET = "LOCAL_PET." + str(i)
command = "r.mapcalc \"%s=(2.1*((%s/12)^2)*%s)/((%s+%s)/2)\"" % (LOCAL_PET, sun_hours, vp_s, tmax_loc, tmin_loc)
print command
os.system(command)

#************************************************************#
# Locally corrected temperature that account for s_i         #
#************************************************************#

#zeros = "zeros." + str(i)
#command = "r.mapcalc \"%s=if(%s>0,0,null())\"" % (zeros, dem_10m)
#os.system(command)

#flat_total_sun = "glob_rad_flat." + str(i)
#command = "r.sun elevin=%s aspin=%s slopein=%s day=%d step=\".05\" dist=\"1\" glob_rad=%s --overwrite" % (dem_10m, zeros, zeros, i, flat_total_sun)
#os.system(command)

#S_i = "S_i." + str(i)
#command = "r.mapcalc \"%s=%s/%s\"" % (S_i, total_sun, flat_total_sun)
#os.system(command)

S_i = S_i + "." + str(i)

tmin_topo = "tmin_topo." + str(i)
command = "r.mapcalc \"%s=%s+(%s-(1/%s))\"" % (tmin_topo, tmin_loc,S_i,S_i)
print command
os.system(command)

tmax_topo = "tmax_topo." + str(i)
command = "r.mapcalc \"%s=%s+(%s-(1/%s))\"" % (tmax_topo, tmax_loc,S_i,S_i)
print command
os.system(command)

#************************************************************#
# Water Balance                                              #
#************************************************************#


#************************************************************#
# PET                                                        #
#************************************************************#
total_sun_joules = "total_sun_joules." + str(i)
command = "r.mapcalc \"%s=%s*3600\"" % (total_sun_joules, total_sun)
print command
os.system(command)

p_a = "p_a." + str(i)
command = "r.mapcalc \"%s=101325*exp(-9.80665*0.289644*%s/(8.31447*288.15))/287.35*((%s+%s/2)+273.125)\"" % (p_a, dem_10m, tmax_topo, tmin_topo)
print command
os.system(command)

f_tmin_topo = "f_tmin_topo." + str(i)
command = "r.mapcalc \"%s=6.108*exp((17.27*%s)/(%s+237.3))\"" % (f_tmin_topo, tmin_topo, tmin_topo)
print command
os.system(command)

f_tmax_topo = "f_tmax_topo." + str(i)
command = "r.mapcalc \"%s=6.108*exp((17.27*%s)/(%s+237.3))\"" % (f_tmax_topo, tmax_topo, tmax_topo)
print command
os.system(command)

vp_s_topo = "vp_s_topo." + str(i)
command = "r.mapcalc \"%s=(%s+%s)/2\"" % (vp_s_topo, f_tmax_topo, f_tmin_topo)
print command
os.system(command)

vp_loc = "vp_loc." + str(i)
command = "r.mapcalc \"%s=6.11*10^(7.5*%s)/(237.3+%s)\"" % (vp_loc,tmin_topo, tmin_topo)
print command
os.system(command)

ra = "ra." + str(i)
command = "r.mapcalc \"%s=(4.72*(exp(2/0.00137))^2)/(1+0.536*5)\"" % (ra)
print command
os.system(command)

m_vp = "m_vp." + str(i)
command = "r.mapcalc \"%s=0.04145*exp(0.06088*(%s+%s/2))\"" % (m_vp, tmax_topo, tmin_topo)
print command
os.system(command)

g_psy = "g_psy." + str(i)
command = "r.mapcalc \"%s=0.001013*(101.3*((293-0.00649*%s)/293)^5.26)/(0.622*2.45)\"" % (g_psy, dem_10m)
print command
os.system(command)

PET = "PET." + str(i)
command = "r.mapcalc \"%s=(%s+%s*0.001013*(%s-%s)/(%s))/(2.45*(%s+%s))\"" % (PET,total_sun_joules,p_a,vp_s_topo,vp_loc,ra,m_vp,g_psy)
print command
os.system(command)

prcp = prcpRaster + "." + str(i)
AET = "AET." + str(i)
command = "r.mapcalc \"%s=%s*(1+%s/%s-(1+(%s/%s)^2.63)^(1/2.63))\"" % (AET,prcp, PET, prcp, PET, prcp)
print command
os.system(command)

#************************************************************#
# EEMT-TOPO                                                  #
#************************************************************#

DT = "DT." + str(i)
command = "r.mapcalc \"%s=((%s+%s)/2)-273.15\"" % (DT, tmax_topo, tmin_topo)
print command
os.system(command)

F = "F." + str(i)
command = "r.mapcalc \"%s=%s*%s\"" % (F, a_i, prcp)
print command
os.system(command)

NPP_trad = "NPP_trad." + str(i)
command = "r.mapcalc \"%s=3000*(1+exp(1.315-0.119*(%s+%s)/2)^-1)\"" % (NPP_trad, tmax_loc, tmin_loc)
print command
os.system(command)

E_bio = "E_bio." + str(i)
command = "r.mapcalc \"%s=%s*(22*10^6)\"" % (E_bio, NPP_trad)
print command
os.system(command)

E_ppt = "E_ppt." + str(i)
command = "r.mapcalc \"%s=%s*4185.5*%s*%s\"" % (E_ppt, F, DT, E_bio)
print command
os.system(command)

EEMT_TOPO = "EEMT_TOPO." + str(i)
command = "r.mapcalc \"%s=%s+%s\"" % (EEMT_TOPO, E_ppt, E_bio)
print command
os.system(command)

