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

Data Collection
==
DEM
OpenTopo: Contains the DEM files which contain latlong points.

Data Storage
==
iPlant/XSEDE

Prepare Data
==


Distribute computations
==
Docker : use it to containerize our apps so that we can run the docker anywhere.


Process Data
==
GRASS : 
QGIS : does some calculations related to water slope models and (maybe) make a predictive analysis of weather change.
EEMT = E_ppt + E_bio (J / (m^2 * s))

Prepare output
==


Output format
==


Visualization
==

