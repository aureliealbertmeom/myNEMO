#If you want to recompile, uncomment the clean option to clean up the dir then compile again

source ~/.bashrc
load_intel

cd /ccc/work/cont003/gen12020/alberaur/DEV/NEMO_5.0/tools/
./maketools -m 'X64_IRENE_XIOS3_2806' -n REBUILD_MPP
