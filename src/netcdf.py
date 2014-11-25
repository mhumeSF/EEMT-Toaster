#!usr/bin/python

import os, sys

class netcdf:
	def __init__(self, year, tiles, param):
		self.year = year
		self.tiles = tiles
		self.param = param
		self.rasters = []
		for tile in tiles:
			self.rasters.append( str(param) + "_" + str(year) + "_" + str(tile) )
		
		self.getNetcdf()
		self.toRaster()
		self.rasterPatch()

	def getNetcdf(self):
		"""
		This be where I use that wet get command to grab images off the intertubes
		"""
		for tile in self.tiles:
			command = "wget -O " + self.param + "_" + str(self.year) + "_" + str(tile) + ".nc " + \
			          "http://thredds.daac.ornl.gov/thredds/fileServer/ornldaac/1219/tiles/" \
					+ str(self.year) + "/" + str(tile) + "_" + str(self.year) + "/" + self.param + ".nc"
			print command
			#replace with os.system(command) when ready
		#try:
		#	print command
            #os.system(command)
		#except:
		#	print "netcdf command did not complete"


	def rasterPatch(self):
		"""
		I patch all the rasters
		"""
		myRasterInput = ",".join(self.rasters)
		myRasterOutput = str(self.param) + "_" + str(self.year) + "_patched"
		command = "g.region rast=" + myRasterInput
		print command
		command = "r.patch input=" + myRasterInput + " output=" + myRasterOutput + " --overwrite"
		print command
		
		self.patchRaster = myRasterOutput

	def toRaster(self):
		for raster in self.rasters:
			command = "r.external -o input=" + raster + ".nc" + " output=" + raster +" --overwrite"
			print command
		#gdal_translate -of GTiFF NETCDF:tmin.nc -b 365 myAwesomeNetCDF
		return

    # netcdf_raster_year_day_a
    # netcdf_raster_year_day_b

    # patch a+b to produce patched raster
