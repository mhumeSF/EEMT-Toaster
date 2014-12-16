#!/bin/bash
## Script to generate temp script to schedule a MPI job

#set -x

usage () {
    echo "Usage: submit <valid_exe_name>" >&2
    exit 1
}

#[ ! -x $1 ] && usage

executable="$1"
command="$@"

script_name="qsub_script_${executable}.pbs"
ncpu=1
job_type="large_mpi"

cat > $script_name << __EOF__
#!/bin/csh
### Set the job name
#PBS -N $executable

### Request email when job begins and ends
################PBS -m bea

### Specify email address to use for notification.
#PBS -M mhume@email.arizona.edu

### Specify the PI group found with va command
#PBS -W group_list=nirav
#PBS -l jobtype=$job_type

### Set the queue to submit this job.
#PBS -q windfall
### Set the number of cpus up to a maximum of 128
#PBS -l select=1:ncpus=1:mem=2gb
#PBS -l pvmem=2gb

### Specify up to a maximum of 1600 hours total cpu time for the job
#PBS -l cput=8:0:0

### Specify up to a maximum of 240 hours walltime for the job
#PBS -l walltime=4:0:0

### Example is: cd ~cihantunc/ece677/mpi/mpi_hello_world/
cd $PWD

source /usr/share/Modules/init/csh
module load intel-mpi

#date
$command
#date
__EOF__

chmod 755 $script_name

qsub $script_name

rm $script_name

#qstat -u $USER