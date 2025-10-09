#!/bin/bash
#SBATCH -J output               # Job name
#SBATCH --nodes 1                # Number of tasks to use
#SBATCH --ntasks 1                # Number of tasks to use
#SBATCH -T 600               # Elapsed time limit in seconds
#SBATCH -o output.o%I           # Standard output. %I is the job id
#SBATCH -e output.e%I           # Error output. %I is the job id
#SBATCH --partition=prepost               # Partition name (see ccc_mpinfo)
#SBATCH -A cli@cpu           # Project ID

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

#Also save namelists and output
mkdir -p SDIR/ANNEX
for file in namelist* ocean.output timing.output; do
	fileo="${file}KK"
	cp $file SDIR/ANNEX/.
done

