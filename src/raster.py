import sys, os, tempfile
# The related files are at $GISBASE/etc/python/grass/script/*.py
from subprocess import call


class raster:

    def __init__(self, tiff, raster):
        """
        This initializes a new instance of a raster object and sets
        the g.region for concurrent raster calculations. It takes two
        arguments, the first is an input geotiff file, the second is a
        name for an output raster file.
        """
        if tiff and raster:
            self.tiff = tiff
            warped = tiff + ".warped"
            self.output = raster

            try:
                #r.external(input=self.tiff, output=self.output)
                os.system("gdalwarp -overwrite -s_srs EPSG:26911 -t_srs \"+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs\" -tr 10 10 -r bilinear -multi -dstnodata 0 -of GTiff %s %s" % (tiff, warped))
                call(["r.external", "input=%s" % (warped), "output=%s" % (self.output), "-o", "--overwrite" ])

            except:
                print("r.external failed to generate raster file "
                        + "with specified input/output names "
                        + self.tiff + " and " + self.output)

            try:
                #g.region(rast=self.output)
                os.system("g.region rast=%s" % (self.output))
            
	    except:
                print("g.region failed to generate output raster file "
                        + "with specified name: " + self.output)
        else:
            print("Missing input tiff or output raster argument")


    def export(self, raster, output):
        """
        This exports the raster files using the command r.external and
        g.region. It takes two arguments, the first is a raster and the second
        is the name of the geoTiff to output as.
        """
        try:
            os.system("r.out.gdal input=%s output=%s" % (raster, output))
        
	except:
            print("r.in.gdal failed to generate your geoTif")

                #r.external(input=myInput, output=myOutput)


    def slopeAspect(self, elevationRaster, outputSlope, outputAspect):
        """
        This method calls the r.slope.aspect function from the grass module.
        It takes three arguments, the first of which is an input elevation raster
        file, the second is an output name for a slope file and the third is an
        output name for an aspect file.
        """
        try:
            command = "r.slope.aspect" \
                + " elevation=" + elevationRaster \
                + " slope=" + outputSlope \
                + " aspect=" + outputAspect \
                + " format=degrees" \
                + " --o"
            os.system(command)

        except:
            print("Failed to run r.slope.aspect with specified arguments")


    def sun(self, myElevRaster, mySlope, myAspect, myDay, myStep, myInsol_time, myGlob_rad):
        """
        This method calls the r.sun function from the grass module. There are a
        ton of arguments for it to run properly.
        """
        try:
            command = (
                "r.sun " + \
                " elevin=" + myElevRaster + \
                " slopein=" + mySlope + \
                " aspin=" + myAspect + \
                " day=" + myDay + \
                " step=" + myStep + \
                " declin=0" + \
                " dist=1" + \
                " -s" + \
                " insol_time=" + myInsol_time + \
                " glob_rad=" + myGlob_rad + \
                " --overwrite"
                )
            os.system(command)

        except:
            print("r.sun failed to run with specified arguments, specifics "
                    + "unknown since there are so many freakin arguments!")


    def mapcalc(self, param, paramRaster, rasterOut, elevRaster, daymetRaster):
        """
        This method calls the r.mapcalc function from the grass module. Its output
        is based on which parameter type is specified. Different calculations are
        done depending on the parameter.
        """
        if param == "tmin":
            lapseRate = 5.69
            tmin = paramRaster
            command = "r.mapcalc %s = %s-(%f/1000*(%s-%s))" % (rasterOut, tmin, lapseRate, elevRaster, daymetRaster)
            os.system(command)

        elif param == "tmax":
            lapseRate = 5.69 # is this the same for tmax?
            tmax = paramRaster
            command = "r.mapcalc %s = %s-(%f/1000*(%s-%s))" % (rasterOut, tmax, lapseRate, elevRaster, daymetRaster)
            os.system(command)

        else:
            print ("Invalid param type")

        # TODO: Add the rest of the equations for each parameter
        #r.mapcalc f_tmin_loc=0.6108*exp((12.27*tmin_loc)/(tmin_loc+237.3))
        #r.mapcalc f_tmax_loc=0.6108*exp((12.27*tmax_loc)/(tmax_loc+237.3))
        #r.mapcalc vp_s=(f_tmax_loc+f_tmin_loc)/2
        #r.mapcalc PET=(2.1*(hours_sun^2)*vp_s/((tmax_loc+tmin_loc)/2)

    #def rPatch(self):
