#!/bin/bash
#SBATCH -J restart               # Job name
#SBATCH --nodes 1                # Number of tasks to use
#SBATCH --ntasks 10                # Number of tasks to use
#SBATCH -T 600               # Elapsed time limit in seconds
#SBATCH -o restart.o%I           # Standard restart. %I is the job id
#SBATCH -e restart.e%I           # Error restart. %I is the job id
#SBATCH --partition=prepost               # Partition name (see ccc_mpinfo)
#SBATCH -A cli@cpu           # Project ID

set -x
source ~/.bashrc
load_intel

cd TMPDIR

PATH_REBUILD/rebuild_nemo BASE DOMAINS
PATH_REBUILD/rebuild_nemo BASE_ice DOMAINS

