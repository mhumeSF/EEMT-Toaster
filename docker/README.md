Build Docker Image
===

The Dockerfile present here builds a base Ubuntu 14.04 image and adds the software that are required to run grass software. To build an image, change to this directory and run the following command
~~~
docker build -t hypercompute:latest .
~~~

Once the image is built, a container can be instantiated by using this command. First change to the root of this repo.
~~~
docker run -i -t -v $PWD/geotiffs:/root/geotiffs -v $PWD/src:/root/scripts hypercompute:latest /bin/bash
~~~

The command line options are as follows:
* -i -> interactive session
* -t -> pseudo terminal
* -v -> specify external directory (ex: $PWD/geotiffs) to mount inside the container (ex: /root/geotiffs)
