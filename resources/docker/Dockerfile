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

# Download Gegraphic Library to do coordinate conversion
RUN wget http://downloads.sourceforge.net/project/geographiclib/distrib/GeographicLib-1.38.tar.gz -P /root/

# Extract the geolib
RUN tar -xzf /root/GeographicLib-1.38.tar.gz -C /root/

# Build the geographic lib
RUN ["/bin/bash", "-c", "cd /root/GeographicLib-1.38/ && make && make install"]
