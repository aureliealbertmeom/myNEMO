#!/bin/bash
#MSUB -r nemo               # Job name
#MSUB -N NODE                # Number of tasks to use
#MSUB -n CORE                # Number of tasks to use
#MSUB -T TIME               # Elapsed time limit in seconds
#MSUB -o nemo.o%I           # Standard output. %I is the job id
#MSUB -e nemo.e%I           # Error output. %I is the job id
#MSUB -q rome               # Partition name (see ccc_mpinfo)
#MSUB -A gen12020           # Project ID
#MSUB -x
#MSUB -m work,scratch

set -x
source ~/.bashrc
load_intel

cd TMPDIR

srun -m cyclic -K1 --multi-prog ./mpmd.conf

nba=$(grep -o 'AAAAAAAA' ocean.output | wc -l)
nbe=$(grep -o 'E R R O R' ocean.output | wc -l)

if [[ "$nbe" -eq '0' ]]; then
        if [[ "$nba" -eq '4' ]]; then
		mkdir -p CONFEXP
		cp *xml namelist* CONFEXP/.
	        ccc_msub job_output.ksh
	        ccc_msub job_restart.ksh
	fi
fi


