###########################################################
#       Dockerfile to build an image to setup Ubuntu      #
#       to run grass commands and parallelize them        #
#       using makeflow/workqueue on different machines    #
###########################################################

# Setting the base image to Ubuntu 14.04
FROM ubuntu:14.04

# Listing the whole team as maintainers
MAINTAINER HotSmokinBarrels

# Expose this port from docker to other ports which is used by Makeflow/Workqueue
EXPOSE 60644

# Create an environment variable that lets us keep port number configurable.
# This env variable shall be used by WQ.
ENV WQPORT 60644

# Update the Ubuntu sources
RUN apt-get update

# Upgrade the base image before continuing
RUN apt-get upgrade -y

# Install the build-essential package which contains tools to compile stuff
RUN apt-get install -y build-essential

# Install the grass package from the official repositories
RUN apt-get install -y grass

# Install wget to download stuff
RUN apt-get install -y wget

# Create a directory to put all downloads and extract sources
RUN mkdir -p /root/sources/

# Download Gegraphic Library to do coordinate conversion
RUN wget http://downloads.sourceforge.net/project/geographiclib/distrib/GeographicLib-1.38.tar.gz -P /root/sources/

# Extract the geolib
RUN tar -xzf /root/sources/GeographicLib-1.38.tar.gz -C /root/sources/

# Build the geographic lib
RUN ["/bin/bash", "-c", "cd /root/sources/GeographicLib-1.38/ && make && make install"]

# Download cctools library
RUN wget http://ccl.cse.nd.edu/software/files/cctools-4.2.2-source.tar.gz -P /root/sources/

# Extract the cctools lib
RUN tar -xzf /root/sources/cctools-4.2.2-source.tar.gz -C /root/sources/

# Install the zlib1g-dev package to provide libz during install
RUN apt-get install zlib1g-dev

# build the cctools package
RUN ["/bin/bash", "-c", "cd /root/sources/cctools-4.2.2-source/ && ./configure && make install"]

# Add cctools to $PATH
RUN ["/bin/bash", "-c", "echo 'export PATH=$PATH:/root/cctools/bin/' >> /root/.bashrc"]
