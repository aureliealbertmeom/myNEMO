#If you want to recompile, uncomment the clean option to clean up the dir then compile again

source ~/.bashrc
load_intel
./makenemo -m 'ARCH' -r REFCONF -n REFCONF_ARCH --add_key 'KEYADD' -j 8  ## --clean_config
