#!/bin/bash
#MSUB -r restart               # Job name
#MSUB -N 1                # Number of tasks to use
#MSUB -n 10                # Number of tasks to use
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

PATH_REBUILD/rebuild_nemo BASE DOMAINS
PATH_REBUILD/rebuild_nemo BASE_ice DOMAINS

