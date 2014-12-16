Overview of the project
==

Please Read: docker/README.md to setup a docker image and instantiate a container.

Different stages of the project:
* Data collection - Plain Download from OpenTOPO
* Data storage - Store on iPlant? FutureGrid? LAX/LAZ files: compressed Lidar Data.
* Prepare data - temp, pressure, etc data, input time, lat/long to get required data.
* Distribute computations - Use Docker/Makeflow to distribute data across HPC/FG/whatever
* Process data - Use formulae to crunch the numbers
* Prepare output - Each docker instance should write its output to files. Directory structure / file name should reflect the organization of data.
* Output format - All inputs, intermediate results and outputs should be put into a csv/json to let data visualization s/w to work on it
* Visualization - TBD


## Data Collection

DEM
OpenTopo: Contains the DEM files which contain latlong points.


## Data Storage

iPlant/XSEDE


## Prepare Data

* Phase 1: Data will be saved as raster files within the grassdata database specified by the user.
* Phase 2: Data will be stored using iRODS if the user chooses to do so.

Warp Geotiff to LCC projection using gdalwarp
Import GRASS raster from Geotiff


## Distribute computations

Actual Implementation:
WorkQueue : Create workers to run r.sun calculations for each day of the year.

Original plan:
Docker : use it to containerize our apps so that we can run the docker anywhere.
*UAHPC / PBS distrobution systems* : Currently tested and working.  Script has the ability to distribute tasks in parallel and report back to the user when tasks are complete.


## Process Data

GRASS : raster map functions to create solar radiation models and localized temperature models *Future products*
QGIS : does some calculations related to water slope models and (maybe) make a predictive analysis of weather change.
EEMT = E_ppt + E_bio (J / (m^2 * s))

## Prepare output

Output will be staged in the given grassdata database file structure

## Output format

Raster maps that are included in the given grassdata database file structure

## Visualization

Under Construction

## User Interfaces

Under Construction
Entry point python script where the user can:
* specify a geotiff or a folder of geotiff files to work on
* specify a range of years to work on
* specify parameters to calculate EEMT (Tmin, Tmax, swe, dayl, etc..)
* specify a time step to use
* specify monthly averages or daily averages

Application Programming Interface
==
Our python scripts were written with extensibility in mind.  The current goal is to have other scientists work with and use our scripts to meet their own ends, therefore, we thought it was important to create types that others can use to extend or build upon what we currently offer here.  An overview of the API can be found here: [https://github.com/mhumeSF/ISTA-420-Midterm/tree/master/src]

