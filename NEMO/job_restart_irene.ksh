#!/bin/bash
#MSUB -r restart               # Job name
#MSUB -N 1                # Number of tasks to use
#MSUB -n 1                # Number of tasks to use
#MSUB -T 600               # Elapsed time limit in seconds
#MSUB -o restart.o%I           # Standard restart. %I is the job id
#MSUB -e restart.e%I           # Error restart. %I is the job id
#MSUB -q xlarge               # Partition name (see ccc_mpinfo)
#MSUB -A gen12020           # Project ID
#MSUB -m work,scratch

set -x
source ~/.bashrc
load_intel

cd TMPDIR
if ls CONFCASE_*NITEND_restart_*nc 1> /dev/null 2>&1; then #in case of millions of files in one dir try compgen -G
	echo 'CONFCASE_NITEND restart files exist'
	nitend8=$(printf "%08d" "NITEND")
	tar -cvf CONFCASE_${nitend8}_restart.tar CONFCASE_*NITEND_restart_*nc
	mv CONFCASE_${nitend8}_restart.tar RDIR/.
	echo ' and have been tared and copyied to RDIR/'
fi


