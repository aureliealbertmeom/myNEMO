#!/bin/bash
#MSUB -r output               # Job name
#MSUB -N 1                # Number of tasks to use
#MSUB -n 1                # Number of tasks to use
#MSUB -T 600               # Elapsed time limit in seconds
#MSUB -o output.o%I           # Standard output. %I is the job id
#MSUB -e output.e%I           # Error output. %I is the job id
#MSUB -q xlarge               # Partition name (see ccc_mpinfo)
#MSUB -A gen12020           # Project ID
#MSUB -m work,scratch

set -x
source ~/.bashrc
load_intel

cd TMPDIR

for freq in 1h 1d 5d 1m 1y; do
	if ls CONFCASE_${freq}_*nc 1> /dev/null 2>&1; then #in case of millions of files in one dir try compgen -G
		echo 'CONFCASE_'$freq' files exist'
		mkdir -p SDIR/$freq
		cp CONFCASE_${freq}_*nc SDIR/$freq/.
		echo ' and have been copyied to SDIR/'$freq
	fi
done


