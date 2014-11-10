#!/bin/bash
## Script to build a docker image and deploy containers running our application.

set -x

err () {
	echo $1 1>&2
	exit
}

check_for_docker () {
	which docker &> /dev/null
	if [ ! $? -eq "0" ]; then
		err "Docker not found."
	fi
}

build_docker() {
	# Build a version that corresponds to the version of dockerfile on the given date
	docker build -t hypercompute:$(date +%Y%m%d) docker/
	# Build it again and tag it as the latest to use to run it
	docker build -t hypercompute:latest docker/
}

run_docker () {
	docker run \
		`# With name of the container as hyper_compute` \
		--name hyper_compute_$(date +%Y_%m_%d_%H_%M_%S) \
		`# Mount a $1 as the folder containing tiffs` \
		-v $1:/root/dems \
		`# Mount the scripts folder` \
		-v $PWD/src:/root/scripts \
		`# From the latest image` \
		hypercompute:latest \
		`# Call this command to start the container` \
		/root/scripts/entryPoint.py
}

main () {
	if [ $# -eq "1" ]; then
		err "Usage: $0 [build/run] <dems_folder>"
	fi

	case $1 in
		"build" )
			build_docker
			;;
		"run" )
			if [ ! $# -eq "2" ]; then
				err "Usage: $0 [build/run] <dems_folder>"
			fi
			run_docker $PWD/$2
			;;
		* )
			err "$1: Invalid operation"
			;;
	esac
}

main $@
