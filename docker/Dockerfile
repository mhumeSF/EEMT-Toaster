###########################################################
#       Dockerfile to build an image to setup Ubuntu      #
#       to run grass commands and parallelize them        #
#       using makeflow/workqueue on different machines    #
###########################################################

# Setting the base image to Ubuntu 14.04
FROM ubuntu:14.04

# Listing the team and maintainer
MAINTAINER HotSmokinBarrels:SriharshaMucheli

# Expose this port from docker to other ports which is used by Makeflow/Workqueue
EXPOSE 60644

# Create environment variablies
# This env variable shall be used as port number by WQ.
ENV WQPORT 60644

# Defining directories
ENV HOME /root
ENV SRCDIR /root/sources
ENV CCTOOLS cctools-4.2.2-source
ENV GEOLIB GeographicLib-1.38
ENV GEODIR /root/sources/$GEOLIB
ENV CCTDIR /root/sources/$CCTOOLS

# Update the Ubuntu sources
RUN apt-get update

# Upgrade the base image before continuing
RUN apt-get upgrade -y

# Install the packages which are required for building or using tools
RUN apt-get install -y build-essential git-core grass wget zlib1g-dev && rm -rf /var/lib/apt/lists/*

# Create a directory to put all downloads and extract sources
RUN mkdir -p /root/sources/

# Download and extract Gegraphic Library
RUN wget -O - http://downloads.sourceforge.net/project/geographiclib/distrib/$GEOLIB.tar.gz | tar xzf - -C $SRCDIR

# Build the geographic lib
RUN ["/bin/bash", "-c", "cd $GEODIR && make && make install"]

# Download and extract cctools library
RUN wget -O - http://ccl.cse.nd.edu/software/files/$CCTOOLS.tar.gz | tar xzf - -C $SRCDIR

# build the cctools package
RUN ["/bin/bash", "-c", "cd $CCTDIR && ./configure && make install"]

# Add cctools and GRASS to $PATH
RUN ["/bin/bash", "-c", "echo 'export PATH=$PATH:/root/scripts/:/root/cctools/bin/:/usr/lib/grass64/bin/' >> /root/.bashrc"]

# Add external files
ADD grassenv /root/
ADD grassrc /root/
RUN ["/bin/bash", "-c", "mv /root/grassrc /root/.grassrc6; echo \"source /root/grassenv\" >> /root/.bashrc"]
