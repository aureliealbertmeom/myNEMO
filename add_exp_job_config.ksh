#bin/bash

add_job=1
add_exp=1
add_config=1

CONFIG=eORCA36.L121
CASE=EXP07

machine=$(cat current_experiment.yml | grep machine | awk '{print $2}')
path_mynemo=$(cat lists.py | grep script_path | grep ${machine} | awk -F\' '{print $4}')
scdir=$(cat lists.py | grep scratch | grep ${machine} | awk -F\' '{print $4}')

cd $path_mynemo

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
	cp ${scdir}/TMPDIR_${CONFIG}-${CASE}/namelist* NEMO/CONFIGS/${CONFIG}/${CONFIG}-${CASE}/.
	cp ${scdir}/TMPDIR_${CONFIG}-${CASE}/*xml NEMO/CONFIGS/${CONFIG}/${CONFIG}-${CASE}/.
fi


