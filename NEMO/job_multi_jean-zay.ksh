#!/bin/bash
#SBATCH -J nemo               # Job name
#SBATCH --nodes NODE                # Number of tasks to use
#SBATCH --ntasks CORE                # Number of tasks to use
#SBATCH -t TIME               # Elapsed time limit in seconds
#SBATCH -o nemo.o%j           # Standard output. %I is the job id
#SBATCH -e nemo.e%j           # Error output. %I is the job id
#SBATCH --partition=cpu_p1               # Partition name (see ccc_mpinfo)
#SBATCH -A cli@cpu           # Project ID
#SBATCH --exclusive

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
	        ccc_msub job_outputKK.ksh
	        ccc_msub job_restartKK.ksh
	fi
fi


