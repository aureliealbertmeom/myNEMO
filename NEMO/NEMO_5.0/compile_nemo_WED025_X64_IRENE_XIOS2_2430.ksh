#If you want to recompile, uncomment the clean option to clean up the dir then compile again

source ~/.bashrc
load_intel
./makenemo -m 'X64_IRENE_XIOS2_2430' -r WED025 -n WED025_X64_IRENE_XIOS2_2430 -j 8 ## --clean
