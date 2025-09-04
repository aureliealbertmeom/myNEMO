#If you want to recompile, uncomment the clean option to clean up the dir then compile again

source ~/.bashrc
load_intel
./makenemo -m 'X64_IRENE_init_XIOS3_2806' -r WED025 -n WED025_wkey_xios3_X64_IRENE_init_XIOS3_2806 --add_key 'key_xios3' -j 8  ## --clean_config
