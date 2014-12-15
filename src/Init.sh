#!/bin/bash

if [[ ! -d $HOME/.local ]]; then
    mkdir $HOME/.local
fi
if [[ ! -d $HOME/.src ]]; then
    mkdir $HOME/.src
fi
cd ~/.src

echo "Installing readline libs..." # Because python wants 'em

URL=https://ftp.gnu.org/gnu/readline/readline-6.0.tar.gz
FILE=$(basename $URL)

echo $FILE
if [[ ! -f $FILE ]]; then
    wget $URL
fi
tar -zxf $FILE > /dev/null
cd readline-6.0
./configure --prefix=$HOME/.local > /dev/null
make -j4 > /dev/null
make install > /dev/null
cd ~/.src

echo "Installing Python 2.7..."  # Because it's 2014

URL=https://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
FILE=$(basename $URL)
if [[ ! -f $FILE ]]; then
    wget $URL
fi
tar -zxf $FILE
cd Python-2.7.3
./configure --prefix=$HOME/.local > /dev/null
make -j4 > /dev/null
make install > /dev/null
cd ~/.src

echo "Installing cctools with work_queue python lib..."

URL=http://ccl.cse.nd.edu/software/files/cctools-4.2.2-source.tar.gz
FILE=$(basename $URL)
if [[ ! -f $FILE ]]; then
    wget $URL
fi
tar -zxf $FILE
cd cctools-4.2.2-source
./configure --prefix $HOME/.local --with-python-path $HOME/.local --with-readline-path $HOME/.local/lib > /dev/null
make -j4 > /dev/null
make install > /dev/null
cd ~/.src

echo "Installing iCommands..." # Why not?

URL=http://www.iplantcollaborative.org/sites/default/files/irods/icommands.x86_64.tar.bz2
FILE=$(basename $URL)
if [[ ! -f $FILE ]]; then
    wget $URL
fi
tar -jxf $FILE
cd icommands
cp i* $HOME/.local/bin/
cd ~/.src

echo "Installing netCDF libs..."

URL=ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.2.tar.gz
FILE=$(basename $URL)
if [[ ! -f $FILE ]]; then
    wget $FILE
fi
./configure --prefix=$HOME/.local --disable-netcdf-4 > /dev/null
make -j4 > /dev/null
make install > /dev/null
cd ~/.src

echo "Installing GDal w/ netCDF support..."
URL=http://download.osgeo.org/gdal/1.11.0/gdal-1.11.0.tar.gz
FILE=$(basename $URL)
if [[ ! -f $FILE ]]; then
    wget $URL
fi
tar -zxf $FILE
cd gdal-1.11.0
./configure --prefix=$HOME/.local > /dev/null
make -j4 > /dev/null
make install > /dev/null
cd ~/.src

echo "Installing Proj libs..."

URL=http://download.osgeo.org/proj/proj-4.8.0.tar.gz
FILE=$(basename $URL)
if [[ ! -f $FILE ]]; then
    wget $URL
fi
tar -zxf $FILE
cd proj-4.8.0
./configure --prefix=$HOME/.local > /dev/null
make -j4 > /dev/null
make install > /dev/null
cd ~/.src

echo "Installing Grass..."

URL=http://grass.osgeo.org/grass64/source/grass-6.4.4.tar.gz
FILE=$(basename $URL)
if [[ ! -f $FILE ]]; then
    wget $URL
fi
tar -zxf $FILE
cd grass-6.4.4
./configure --prefix=$HOME/.local --with-proj-libs=$HOME/.local/lib --with-proj-includes=$HOME/.local/include --with-fftw=no > /dev/null
make -j4 > /dev/null
make -j4 > /dev/null # Error for wxpython that is resolved if I run make once more. Order of operations?

make install

cd

echo 'export GISBASE="$HOME/.local/grass-6.4.4/"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$HOME/bin:$GISBASE/bin:$GISBASE/scripts:$PATH"' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH="$HOME/.local/grass-6.4.4/lib:$HOME/.local/lib"' >> ~/.bashrc
echo 'export GRASS_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"' >> ~/.bashrc
echo 'export GISRC=$HOME/.grassrc' >> ~/.bashrc
echo 'export GIS_LOCK=/tmp/grass_lock' >> ~/.bashrc