#bin/bash

cd /ccc/work/cont003/gen12020/alberaur/DEV/myNEMO

add_job=0
add_exp=0
add_config=1

CONFIG=eORCA05.L121
CASE=EXP07

if [ $add_job -eq 1 ]; then
	cp current_job.yml tmp.yml
	cat _data/all_jobs.yml >> tmp.yml
	mv tmp.yml _data/all_jobs.yml
fi

if [ $add_exp -eq 1 ]; then
	cp current_experiment.yml tmp.yml
	cat _data/all_experiments.yml >> tmp.yml
	mv tmp.yml _data/all_experiments.yml
fi

if [ $add_config -eq 1 ]; then
	mkdir -p NEMO/CONFIGS/${CONFIG}/${CONFIG}-${CASE}
	cp /ccc/scratch/cont003/gen12020/alberaur/TMPDIR_${CONFIG}-${CASE}/namelist* NEMO/CONFIGS/${CONFIG}/${CONFIG}-${CASE}/.
	cp /ccc/scratch/cont003/gen12020/alberaur/TMPDIR_${CONFIG}-${CASE}/*xml NEMO/CONFIGS/${CONFIG}/${CONFIG}-${CASE}/.
fi


