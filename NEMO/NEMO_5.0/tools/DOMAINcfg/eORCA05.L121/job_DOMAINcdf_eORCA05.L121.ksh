#!/bin/bash
#MSUB -r DOMAINcfg               # Job name
#MSUB -N 1                # Number of tasks to use
#MSUB -n 20                # Number of tasks to use
#MSUB -T 7200               # Elapsed time limit in seconds
#MSUB -o DOMAINcfg.o%I           # Standard output. %I is the job id
#MSUB -e DOMAINcfg.e%I           # Error output. %I is the job id
#MSUB -q rome               # Partition name (see ccc_mpinfo)
#MSUB -A gen12020           # Project ID
#MSUB -x
#MSUB -m work,scratch

set -x
source ~/.bashrc
load_intel

cd /ccc/work/cont003/gen12020/alberaur/eORCA05.L121/eORCA05.L121-I/DOMAINcfg

srun -n 20 ./make_domain_cfg.exe

rebuild_nemo domain_cfg 20
rebuild_nemo mesh_mask 20

ncks -O -4 -L 1 --cnk_dmn z,1 domain_cfg.nc domain_cfg.nc4
ncks -O -F -4 -L 1 --cnk_dmn x,720 --cnk_dmn y,100 -d x,2,721 -d y,1,603 domain_cfg.nc4 eORCA05.L121_domain_cfg.nc

ncks -O -4 -L 1 --cnk_dmn z,1 mesh_mask.nc mesh_mask.nc4
ncks -O -F -4 -L 1 --cnk_dmn x,720 --cnk_dmn y,100 -d x,2,721 -d y,1,603 mesh_mask.nc4 eORCA05.L121_mesh_mask.nc

cp eORCA05.L121_domain_cfg.nc ../eORCA05.L121_domain_cfg_v2025.nc
cp eORCA05.L121_mesh_mask.nc ../eORCA05.L121_mesh_mask_v2025.nc
