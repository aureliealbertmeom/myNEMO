#bin/bash

list_exp='eORCA36.L121-EXP01 eORCA36.L121-EXP02 eORCA36.L121-EXP03 eORCA36.L121-EXP04 eORCA36.L121-EXP05 eORCA36.L121-EXP06 eORCA36.L121-EXP09 eORCA36.L121-EXP10'

for exp in $list_exp; do
	CONFIG=$(echo $exp | awk -F- '{print $1}')
	CASE=$(echo $exp | awk -F- '{print $2}')
	echo 'adding '$CONFIG $CASE' to the catalog'

	if [ ! -f content/configurations/${CONFIG}.md ]; then
		cp content/configurations/CONF.template content/configurations/${CONFIG}.md
		sed -i "s/CONF/${CONFIG}/g" content/configurations/${CONFIG}.md
		cp _includes/list_config_CONF.template _includes/list_config_${CONFIG}.html
		sed -i "s/CONF/${CONFIG}/g" _includes/list_config_${CONFIG}.html
	fi

	if [ ! -f content/experiments/${exp}.md ]; then
		cp content/experiments/CONF-CASE.template content/experiments/${exp}.md
		sed -i "s/CONFCASE/${exp}/g" content/experiments/${exp}.md
		cp _includes/experiment_CONFCASE.template _includes/experiment_${exp}.html
		sed -i "s/CONFCASE/${exp}/g" _includes/experiment_${exp}.html
	fi

done


