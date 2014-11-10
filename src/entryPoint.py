from raster import raster
from work_queue import *
from geotiff import *

import os
import sys

rmapOutputDirectories = ("/cats", "/cell", "/cellhd", \
						 "/cell_misc", "/color", "/fcell" \
						 "/hist")

if __name__ == '__main__':

	
	port = 0
  
	if len(sys.argv) < 2:
		print "entryPoint [input] [year]"
		
		sys.exit(1)
	
	input =    sys.argv[1]
	year = sys.argv[2]
	
	
	try:
		q = WorkQueue(port)
	except:
		print "Instantiation of Work Queue failed!" 
		sys.exit(1)
	
	geo = geotiff(input)
	
	warptiff = input + "_warp"
	geo.gdalwarp(input, warptiff)
	
	# do we need to run sun on the warp tiff or not?
	elevRaster = warptiff + "_raster"
	try:
		r = raster(warptiff, elevRaster)
	except:
		print "Cannot create raster: " + elevRaster
		sys.exit(1)
	
	slope = elevRaster + "_slope"
	aspect = elevRaster + "_aspect"
	try:
		r.slopeAspect(elevRaster, slope, aspect)
	except:
		print "Cannot create slope and aspect: " + slope + " " + aspect
		sys.exit(1)
	
	#r.sun( #   elevationRaster=myElevationRaster,
        #   slope=mySlope,
        #   aspect=myAspect,
        #   day=myDay,
        #   step=myStep,
        #   declin="0",
        #   dist="1",
        #   insol_time=myInsol_time,
        #   glob_rad=myGlob_rad,
        #   flags="s",
        #   overwrite=true
        #   )
	
	endDay = 367 if (year % 4) == 0 else 366

	for day in range(1,endDay):
	
		insole_time = elevRaster + "_" + year + "_" + day
		glob_rad = elevRaster + "_" + year + "_" + day
 
		command = "python sun.py " + \
		          " elevationRaster=" + elevRaster + \
				  " slope=" + slope + \
				  " aspect=" + aspect + \
				  " day=" + day + \
				  " step=" + step + \
				  " declin=\"0\"" + \
				  " dist=\"1\"" + \
				  " insol_time=" + insol_time + \
				  " glob_rad=" + glob_rad + \
				  " -s --overwrite"
		t = Task(command)
		
		# do we need an absolute path?
		#pythonPath = "/usr/local/bin"
		#t.specify_file(pythonPath, "python", WORK_QUEUE_INPUT, cache=True)
		#t.specify_file("sun.py", "sun.py", WORK_QUEUE_INPUT, cache=False)
		
		# we might need these from the user..
		"""
		grassdataPath = ""
		Location = ""
		Mapset = ""
		basePath = grassdataPath + "/" + Location + "/" + Mapset
		
		for s in rmapOutputDirectories:
			rasterPath = basePath + s
			t.specify_file(rasterPath, insol_time, WORK_QUEUE_OUTPUT, cache=False)
			t.specify_file(rasterPath, glob_rad, WORK_QUEUE_OUTPUT, cache=False)
		"""
		taskid = q.submit(t)
		print "submitted task (id# %d): %s" % (taskid, t.command)
		
	print "listening on port %d..." % q.port

	while not q.empty():
		t = q.wait(5)
		if t:
			print "task (id# %d) complete: %s (return code %d)" % (t.id, t.command, t.return_status)
			if t.return_status != 0:
        # The task failed. Error handling (e.g., resubmit with new parameters, examine logs, etc.) here
        #None
	#task object will be garbage collected by Python automatically when it goes out of scope

	print "all tasks complete!"

	#work queue object will be garbage collected by Python automatically when it goes out of scope
	sys.exit(0)
