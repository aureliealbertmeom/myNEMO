#!/bin/bash
#SBATCH -J restart               # Job name
#SBATCH --nodes 1                # Number of tasks to use
#SBATCH --ntasks 1                # Number of tasks to use
#SBATCH -T 600               # Elapsed time limit in seconds
#SBATCH -o restart.o%I           # Standard restart. %I is the job id
#SBATCH -e restart.e%I           # Error restart. %I is the job id
#SBATCH --partition=prepost               # Partition name (see ccc_mpinfo)
#SBATCH -A cli@cpu          # Project ID

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


