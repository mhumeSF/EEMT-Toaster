### paramcalc.py

##### Usage:

	$ python paramcalc param=tmin paramValue=$tmin rasterout=tmin_loc elevationRaster=sosierra_warp daymetRaster=na_dem

##### Inputs:
- **param** is the daymet data type we’ll be working on: param=tmin, tmax, swe, vp, day
- **rasterout** is the name of the file that will contain the output raster.
- **elevationRaster** is the raster map of the openTopo data being worked on.
- **daymetRaster** is the raster map of the 1KM daymet dem (na_dem).

##### Description:
The idea is to resume this script for each of the parameter calculations we need to make. This script if written correctly, will work for every piece of daymet data obtained from the CSV file.



### slopeaspect.py

##### Usage:

	$ python slopeaspect.py elevationRaster=sosierra_warp slope=slop aspect=aspect

##### Inputs:
- **elevationRaster** is the raster map obtained by OpenTopo that we’re currently working on
- **slope** is the slope raster outfile
- **aspect** is the aspect raster outfield

##### Description:
This will simply call r.slope.aspect and out slope and aspect rasters for r.sun


### importraster.py

##### Usage:

	$ python importraster.py input=geoTiff output=raster

##### Inputs:
- **input** The input geoTiff to be used for concurrent calculations
- **output** The name of the raster file to output (use this as the input to sun, paramcalc etc)

##### Description:
Creates a raster file and sets the g.region for Concurrent raster calculations



### sun.py

##### Usage:

	$ python sun.py elevationRaster=elevationRaster slope=slope aspect=aspect day=day step=step beam_rad=beam_rad insol_time=insol_time diff_rad=diff_rad refl_rad=refl_rad glob_rad=glob_rad

##### Inputs:
- **elevationRaster** the OpenTopo elevation raster
- **slope** slope input from previous
- **aspect** aspect input from previous
- **day** current day we’re working on
- **step** time step (this is in hours so Tysonsiad 0.05 is about every 4 minutes)
- **beam_rad** beam_rad raster outfile
- **insol_time** sol_time raster outfile
- **refl_rad** refl_rad outfile
- **glob_rad** glob_rad outfile

##### Description:
Ok, this is essentially the heart of the project. The loop to run this script is going to have to come from outside so it can be parallelized. The input parameters are fairly simple — the slope and aspect models obtained from slopeaspect.py, the day in which to work on and the step value. Also the out files (I don’t know if tyson needs all of these, but he included them  in his guy example, so we’re going to include them) beam_rad, insol_time, diff_rad, refl_rad and glob_rad. I believe these are all different kinds of radiation maps. I’m going to leave Tyson’s example below for reference purposes.

	r.sun elevin=tmp1414703925037 aspin=tmp1414703925038 slopein=tmp1414703925039 day="1" step="0.5" declin="0" dist="1" ­-s beam_rad=beam_rad7a3de19caf71412e9703e50b15d252d7 insol_time=insol_time7a3de19caf71412e9703e50b15d252d7 diff_rad=diff_rad7a3de19caf71412e9703e50b15d252d7 refl_rad=refl_rad7a3de19caf71412e9703e50b15d252d7 glob_rad=glob_rad7a3de19caf71412e9703e50b15d252d7 ­­overwrite
