#!/bin/csh
### Set the job name
#PBS -N dspence_wq

### Request email when job begins and ends
#PBS -m bea

### Specify email address to use for notification.
#PBS -M dspence@email.arizona.edu

### Specify the PI group found with va command
#PBS -W group_list=nirav
#PBS -l jobtype=serial

### Set the queue to submit this job.
#PBS -q standard
### Set the number of cpus up to a maximum of 128
#PBS -l select=1:ncpus=1:mem=1gb
#PBS -l pvmem=1gb

### Specify up to a maximum of 1600 hours total cpu time for the job
#PBS -l cput=1:0:0

### Specify up to a maximum of 240 hours walltime for the job
#PBS -l walltime=1:0:0

cd /home/u13/dspence/ISTA-420-Midterm/src/dspence-workers

source /usr/share/Modules/init/csh

./work_queue_worker  -M eemt_toaster  
