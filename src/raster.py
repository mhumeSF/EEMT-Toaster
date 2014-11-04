import sys
import os
import tempfile
# The related files are at $GISBASE/etc/python/grass/script/*.py
import grass.script as grass
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules import Module
from grass.pygrass.modules.shortcuts import general as g

class raster:

    """
    This initializes a new instance of a raster object and sets
    the g.region for concurrent raster calculations. It takes two
    arguments, the first is an input geotiff file, the second is a
    name for an output raster file.
    """
    def __init__(self, tiff, raster):
        if tiff and raster:
            self.tiff = tiff
            self.output = raster
            try:
                r.external(input=self.tiff, output=self.output)
            except:
                print("r.external failed to generate raster file "
                    + "with specified input/output names "
                    + self.tiff + " and " + self.output)

            try:
                g.region(rast=self.output)
            except:
                print("g.region failed to generate output raster file "
                    + "with specified name: " + self.output)
        else:
            print("Missing input tiff or output raster argument")


    """
    This exports the raster files using the command r.external and
    g.region. It takes two arguments, the first is a
    """
    """
    def export(self, ):
        for arg in sys.argv:
		    mySplit = arg.split('=')
		    if len(mySplit) > 1:
			    command = mySplit[0]
			    value = mySplit[1]
			    if command = "input":
				    myInput = value
			    if command = "output":
				    myOutput = value

        r.external(input=myInput, output=myOutput)
        g.region(rast=myOutput)
    """


    """
    This method calls the r.slope.aspect function from the grass module.
    It takes three arguments, the first of which is an input elevation raster
    file, the second is an output name for a slope file and the third is an
    output name for an aspect file.
    """
    def slopeAspect(self, elevRaster, outputSlope, outputAspect):
        try:
            # call r.slope.aspect
            slope_aspect = Module("r.slope.aspect")
            slope_aspect(elevation=elevationRaster, slope=outputSlope,
                         aspect=outputAspect, format='degrees', overwrite=True)
        except:
            print("Failed to run r.slope.aspect with specified arguments")


    """
    This method calls the r.sun function from the grass module. There are a
    ton of arguments for it to run properly.
    """
    def rSun(self, myElevRaster, mySlope, myAspect, myDay, myStep, myBeam_rad,
             myInsol_time, myDiff_rad, myRefl_rad, myGlob_rad):
        try:
            # call r.sun
	        r.sun(elevationRaster=MyElevRaster, slope=mySlope,
	          aspect=myAspect, day=myDay step=myStep, declin="0"
	          dist="1", beam_rad=myBeam_rad, insol_time=myInsol_time,
		      diff_rad=myDiff_rad, refl_rad=myRefl_rad,
		      glob_rad=myGlob_rad flags="s" overwrite=true)
        except:
            print("r.sun failed to run with specified arguments, specifics "
                + "unknown since there are so many freakin arguments!")


    """
    This method calls the r.mapcalc function from the grass module. Its output
    is based on which parameter type is specified. Different calculations are
    done depending on the parameter.
    """
    def rMapcalc(self, param, paramRaster, rasterOut, elevRaster, daymetRaster):
	        if param == "tmin":
		        lapseRate = 5.69
		        tmin = paramRaster
		        r.mapcalc( "%s = %s-(%f/1000*(%s-%s))" % rasterOut,
		                  tmin, lapseRate, elevRaster,
		                  daymetRaster )
	        if param == "tmax":
		        lapseRate = 5.69 # is this the same for tmax?
		        tmax = paramRaster
		        r.mapcalc( "%s = %s-(%f/1000*(%s-%s))" % rasterout,
		                  tmax, lapseRate, elevRaster,
		                  daymetRaster )
	        else:
		        print "Invalid param type"

	        # TODO: Add the rest of the equations for each parameter

    #def rPatch(self):


