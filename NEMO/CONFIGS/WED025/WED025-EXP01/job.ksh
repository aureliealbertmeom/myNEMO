#!/bin/bash
#MSUB -r nemo               # Job name
#MSUB -n 32                # Number of tasks to use
#MSUB -T 7200               # Elapsed time limit in seconds
#MSUB -o nemo.o%I           # Standard output. %I is the job id
#MSUB -e nemo.e%I           # Error output. %I is the job id
#MSUB -q rome               # Partition name (see ccc_mpinfo)
#MSUB -A gen12020           # Project ID
#MSUB -m work,scratch

set -x
source ~/.bashrc
load_intel

cd /ccc/scratch/cont003/gen12020/alberaur/TMPDIR_WED025-EXP01

ccc_mprun ./nemo


