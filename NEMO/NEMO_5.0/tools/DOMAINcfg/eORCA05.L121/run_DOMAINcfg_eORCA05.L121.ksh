ln -sf ../eORCA05_coordinates.nc coordinates.nc
ln -sf ../eORCA05_bathymetry_b0.5-v2.nc bathy_meter.nc

ln -sf /ccc/work/cont003/gen12020/alberaur/DEV/NEMO_5.0/tools/REBUILD_NEMO/rebuild_nemo .
ln -sf /ccc/work/cont003/gen12020/alberaur/DEV/NEMO_5.0/tools/REBUILD_NEMO/rebuild_nemo.exe .

ccc_msub job_DOMAINcdf_eORCA05.L121.ksh
