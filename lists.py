#Lists


#Relative to running NEMO

all_machine=['irene','jean-zay']
all_jobsub_machine={}
all_jobsub_machine['irene']='ccc_msub'
all_jobsub_machine['jean-zay']='sbatch'

all_path_dev={}
all_path_dev['irene']='/ccc/work/cont003/gen12020/alberaur/DEV'
all_path_dev['jean-zay']='/lustre/fswork/projects/rech/cli/rote001/DEV'

all_path_work={}
all_path_work['irene']='/ccc/work/cont003/gen12020/alberaur'
all_path_work['jean-zay']='/lustre/fswork/projects/rech/cli/rote001'

all_path_scratch={}
all_path_scratch['irene']='/ccc/scratch/cont003/gen12020/alberaur'
all_path_scratch['jean-zay']='/lustre/fsn1/projects/rech/cli/rote001'

script_path={}
script_path['irene']='/ccc/work/cont003/gen12020/alberaur/DEV/myNEMO'
script_path['jean-zay']='/lustre/fswork/projects/rech/cli/rote001/DEV/myNEMO'

all_path_store={}
all_path_store['irene']='/ccc/store/cont003/gen12020/alberaur'
all_path_store['jean-zay']='/lustre/fsstor/projects/rech/cli/rote001'

all_compiler={}
all_compiler['irene']='intel'
all_compiler['jean-zay']='intel'

all_arch_xios={}
all_arch_xios['irene']=['X64_IRENE']
all_arch_xios['jean-zay']=['X64_JEANZAY']

all_arch_nemo={}
all_arch_nemo['irene']=['X64_IRENE','X64_IRENE_debug']
all_arch_nemo['jean-zay']=['X64_JEANZAY']

all_tag_xios={}
all_tag_xios['irene']=['XIOS3_2656','XIOS2_2430','XIOS3_2806']
all_tag_xios['jean-zay']=['XIOS3_2806']

all_path_xios={}
all_path_xios['irene']={}
all_path_xios['irene']['XIOS3_2806']=all_path_dev['irene']+'/xios3-trunk-2806'
all_path_xios['irene']['XIOS3_2656']=all_path_dev['irene']+'/xios3-trunk-2656'
all_path_xios['irene']['XIOS2_2430']=all_path_dev['irene']+'/xios-trunk-2430'
all_path_xios['jean-zay']={}
all_path_xios['jean-zay']['XIOS3_2806']=all_path_dev['jean-zay']+'/xios3-trunk-2806'

all_tag_nemo={}
all_tag_nemo['irene']=['NEMO_4.2.2','NEMO_5.0']
all_tag_nemo['jean-zay']=['NEMO_5.0']

all_path_nemo={}
all_path_nemo['irene']={}
all_path_nemo['jean-zay']={}
all_path_nemo['jean-zay']['NEMO_5.0']='/lustre/fswork/projects/rech/cli/rote001/DEV/NEMO_5.0'
for tag_nemo in all_tag_nemo['irene']:
    all_path_nemo['irene'][tag_nemo]=all_path_dev['irene']+'/'+str(tag_nemo)

all_ref_conf_nemo={}
all_ref_conf_nemo['NEMO_4.2.2']=['AGRIF_DEMO','AMM12','C1D_PAPA','GYRE_BFM','GYRE_PISCES',
                       'ORCA2_ICE_PISCES','ORCA2_OFF_PISCES','ORCA2_OFF_TRC',
                       'ORCA2_SAS_ICE','SPITZ12','WED025','X3_ORCA2_ICE']

all_geo_ref_conf_nemo={}
all_geo_ref_conf_nemo['WED025']='WED025'
all_geo_ref_conf_nemo['X3_ORCA2_ICE']='ORCA2'

all_geo_conf_nemo={}
all_geo_conf_nemo['irene']=['ORCA2','WED025','eORCA05.L121','eORCA36.L121']
all_geo_conf_nemo['jean-zay']={}

all_comp_nemo={}
all_comp_nemo['irene']={}
all_comp_nemo['jean-zay']={}
all_comp_nemo['jean-zay']['NEMO_5.0']=['WED025_wkey_xios3_X64_JEANZAY_XIOS3_2806','WED025_wkey_xios3_X64_JEANZAY_debug_XIOS3_2806']
all_comp_nemo['irene']['NEMO_4.2.2']=['WED025_X64_IRENE_XIOS2_2430','X3_ORCA2_ICE_X64_IRENE_XIOS3_2656','WED025_X64_IRENE_XIOS2_2430']
all_comp_nemo['irene']['NEMO_5.0']=['X3_ORCA2_ICE_PISCES','X3_ORCA2_ICE_PISCES_X64_IRENE_XIOS3_2806','WED025_X64_IRENE_XIOS2_2430','WED025_wkey_xios3_X64_IRENE_XIOS3_2806','WED025_wkey_xios3_X64_IRENE_debug_XIOS3_2806','WED025_wkey_xios3_X64_IRENE_init_XIOS3_2806','WED025_wkey_xios3_X64_IRENE_debugO3_XIOS3_2806']

all_exp_config_nemo={}
all_exp_config_nemo['irene']={}
all_exp_config_nemo['jean-zay']={}
all_exp_config_nemo['irene']['NEMO_4.2.2']={}
all_exp_config_nemo['irene']['NEMO_4.2.2']['WED025_X64_IRENE_XIOS2_2430']={}

all_tools={}
all_tools['irene']={}
all_tools['jean-zay']={}
all_tools['irene']['NEMO_5.0']=['REBUILD_NEMO','DOMAINcfg']

all_exec_tool={}
all_exec_tool['REBUILD_NEMO']=['rebuild_nemo.exe']
all_exec_tool['DOMAINcfg']=['make_domain_cfg.exe','dom_doc.exe']

all_nam_tool={}
all_nam_tool['REBUILD_NEMO']=['nam_rebuild']
all_nam_tool['DOMAINcfg']=['namelist_cfg','namelist_ref']

all_nam_tool
#Relative to stored simulations for slice and plots

configuration_list={}
configuration_list['irene']=['eORCA05.L121']

simulation_list={}
simulation_list['irene']={}
simulation_list['irene']['eORCA05.L121']='EXP07'

directory={}
directory['irene']={}
directory['irene']['eORCA05.L121']={}
directory['irene']['eORCA05.L121']['EXP07']='/ccc/work/cont003/gen12020/alberaur/eORCA05.L121/eORCA05.L121-EXP07-S'

stylenom={}
stylenom['irene']={}
stylenom['irene']['eORCA05.L121']={}
stylenom['irene']['eORCA05.L121']['EXP07']='brodeau_enatl'

maskfile={}
maskfile['irene']={}
maskfile['irene']['eORCA05.L121']={}
maskfile['irene']['eORCA05.L121']['global']='/ccc/work/cont003/gen12020/alberaur/eORCA05.L121/eORCA05.L121-I/eORCA05.L121_mesh_mask_v2025.nc'

mesh_hgr={}
mesh_hgr['irene']={}
mesh_hgr['irene']['eORCA05.L121']={}
mesh_hgr['irene']['eORCA05.L121']['global']='/ccc/work/cont003/gen12020/alberaur/eORCA05.L121/eORCA05.L121-I/eORCA05.L121_mesh_mask_v2025.nc'

mesh_zgr={}
mesh_zgr['irene']={}
mesh_zgr['irene']['eORCA05.L121']={}
mesh_zgr['irene']['eORCA05.L121']['global']='/ccc/work/cont003/gen12020/alberaur/eORCA05.L121/eORCA05.L121-I/eORCA05.L121_mesh_mask_v2025.nc'

maskfile={}
maskfile['irene']={}
maskfile['irene']['eORCA05.L121']={}
maskfile['irene']['eORCA05.L121']['global']='/ccc/work/cont003/gen12020/alberaur/eORCA05.L121/eORCA05.L121-I/eORCA05.L121_mesh_mask_v2025.nc'

bathyfile={}
bathyfile['irene']={}
bathyfile['irene']['eORCA05.L121']={}
bathyfile['irene']['eORCA05.L121']['global']='/ccc/work/cont003/gen12020/alberaur/eORCA05.L121/eORCA05.L121-I/eORCA05.L121_mesh_mask_v2025.nc'

regions_list={}
regions_list['eORCA05.L121']=['eORCA','global']
regions_list['eORCA36.L121']=['eORCA','global','natl','satl','arctic','antarctic','indian','windian','eindian','npac','spac','med','npole','spole','eqpac','madagascar','bassas','glorieuses','juan','tromelin','mascaraignes']

xy={}
xy['eORCA36.L121']={}
xy['eORCA05.L121']={}
xy['eORCA05.L121']['global']=[0,719,0,602]
xy['eORCA36.L121']['global']=[0,12959,0,10841]
xy['eORCA36.L121']['natl']=[6732,10504,6152,8924]
xy['eORCA36.L121']['satl']=[7812,11052,3436,6152]
xy['eORCA36.L121']['windian']=[11052,12959,3436,7292]
xy['eORCA36.L121']['eindian']=[0,1693,3436,7292]
xy['eORCA36.L121']['npac']=[972,7500,6152,8996]
xy['eORCA36.L121']['spac']=[2500,7812,3436,6152]
xy['eORCA36.L121']['med']=[9972,12042,7289,8400]
xy['eORCA36.L121']['eqpac']=[1972,7500,6152,6152]


vars_name={}
vars_name['eORCA05.L121']={}
vars_name['eORCA05.L121']['EXP07']={'SSH':'zos','SSU':'uos','SSV':'vos','SSS':'sos','SST':'tos','U':'vozocrtx','V':'vomecrty','W':'vovecrtz',
                                     'S':'vosaline','T':'votemper','SICONC':'siconc','SITHIC':'sithic','MLD':'somxl010','TAUM':'taum','QSROCE':'qsr_oce',
                                     'QNSOCE':'qns_oce','PRECIP':'sowapre','WINDSP':'sowinsp','NETDHEATFLX':'sohefldo','SWDHEATFLX':'soshfldo',
                                     'QNS':'qns','LDHEATFLX':'solhflup','LWDHEATFLX':'solwfldo','SDHEATFLX':'sosbhfup','NETUPWFLX':'sowaflup',
                                     'DSALTFLX':'sosfldow','DAMPWFLX':'sowafld'}
filetyp={}
filetyp['eORCA05.L121']={}
for simu in ['EXP07']:
    filetyp['eORCA05.L121'][simu]={}
    for var in ['SSH','SSS','SST','T','S','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP',
                'RHOAIR','MLD','MOD','VORT','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX','SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX']:
        filetyp['eORCA05.L121'][simu][var]='gridT'
    for var in ['SSU','U','SBU','TAUUO']:
        filetyp['eORCA05.L121'][simu][var]='gridU'
    for var in ['SSV','V','SBV','TAUVO']:
        filetyp['eORCA05.L121'][simu][var]='gridV'
    filetyp['eORCA05.L121'][simu]['W']='gridW'
    for var in ['SICONC','SITHIC']:
        filetyp['eORCA05.L121'][simu][var]='icemod'

frequencies={}
frequencies['eORCA05.L121']={}
frequencies['eORCA05.L121']['EXP07']={'SSH':'1h','SSU':'1h','SSV':'1h','SSS':'1h','SST':'1h','MLD':'1h','SICONC':'1h','SITHIC':'1h','MOD':'1h','VORT':'1h','U':'12h','V':'12h','S':'12h','T':'12h','W':'12h','NETDHEATFLX':'1h','NETUPWFLX':'1h','PRECIP':'1h','WINDSP':'1h','SWDHEATFLX':'1h','LWDHEATFLX':'1h'}

frequencies_file={}
frequencies_file['eORCA05.L121']={}
frequencies_file['eORCA05.L121']['EXP07']={'NETDHEATFLX':'12h','NETUPWFLX':'12h','PRECIP':'12h','WINDSP':'12h','SWDHEATFLX':'12h','LWDHEATFLX':'12h',
                     'SSH':'12h','SSU':'12h','SSV':'12h','SSS':'12h','SST':'12h','MLD':'12h','SICONC':'12h','SITHIC':'12h','MOD':'12h','VORT':'12h',
                     'U':'12h','V':'12h','S':'12h','T':'12h','W':'12h'}

sim_date_init={}
sim_date_end={}
sim_date_init['eORCA05.L121']={}
sim_date_end['eORCA05.L121']={}
sim_date_init['eORCA05.L121']['EXP07']='2012-01-01 01:00'
sim_date_end['eORCA05.L121']['EXP07']='2012-12-31 23:00'

#Generic stuff about variables adn grids

variable_list=['SSH','SSU','SSV','SSS','SST','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE',
               'EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','MOD','VORT','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX',
               'LWDHEATFLX','SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX','bathy','MOC','u10','v10','u10m','v10m','BOTU','BOTV','buoyancy','mask','curloverf']


vars_dim={}
for var in ['SSH','SSU','SSV','SSS','SST','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP',
            'RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX','SDHEATFLX',
            'NETUPWFLX','DSALTFLX','DAMPWFLX','MOD','VORT','bathy','MOC','u10','v10','u10m','v10m','BOTU','BOTV']:
    vars_dim[var]='2D'
for var in ['T','S','U','V','W','buoyancy','curloverf']:
    vars_dim[var]='3D'

depname={}
for var in ['T','S','MOD','VORT','buoyancy']:
    depname[var]='deptht'
for var in ['U','curloverf'] :
    depname[var]='depthu'
for var in ['V'] :
    depname[var]='depthv'
for var in ['W','MOC'] :
    depname[var]='depthw'

e1name={}
for var in ['T','S','MOD','VORT','buoyancy']:
    e1name[var]='e1t'
for var in ['U','curloverf'] :
    e1name[var]='e1u'
for var in ['V'] :
    e1name[var]='e1v'
for var in ['W','MOC'] :
    e1name[var]='e1f'

e2name={}
for var in ['T','S','MOD','VORT','buoyancy']:
    e2name[var]='e2t'
for var in ['U','curloverf'] :
    e2name[var]='e2u'
for var in ['V'] :
    e2name[var]='e2v'
for var in ['W','MOC'] :
    e2name[var]='e2f'

e3name={}
for var in ['T','S','MOD','VORT','buoyancy']:
    e3name[var]='e3t_0'
for var in ['U','curloverf'] :
    e3name[var]='e3u_0'
for var in ['V'] :
    e3name[var]='e3v_0'
for var in ['W','MOC'] :
    e3name[var]='e3w_0'

varpt={'T':'T','S':'T','SSH':'T','SST':'T','SSS':'T','SSU':'U','SSV':'V','U':'U','V':'V','W':'W','TAUM':'T','TAUBOT':'T','QTOCE':'T','QSROCE':'T',
       'QSBOCE':'T','QNSOCE':'T','QLWOCE':'T','QLAOCE':'T','PRECIP':'T','EVAPOCE':'T','EMPMR':'T','WINDSP':'T','RHOAIR':'T','MLD':'T','BOTU':'U',
       'TAUUO':'U','BOTV':'V','TAUVO':'V','u10':'U','v10':'V','u10m':'U','v10m':'V','curloverf':'U'}

compute={}
for var in ['SSH','SSU','SSV','SSS','SST','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE',
            'EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX',
            'SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX','MOC','u10','v10']:
    compute[var]=False
for var in ['MOD','VORT']:
    compute[var]=True

compute_vars={}
for var in ['MOD','VORT']:
    compute_vars[var]=['U','V']

#Relative to plots
#import cmocean

latlon_lims={}
latlon_lims={}
latlon_lims['global']=[-180,180,-90,90]

compute={} #when a variable is a computation between several variables
for var in ['SSH','SSU','SSV','SSS','SST','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE',
            'EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO','SICONC','SITHIC','NETDHEATFLX','SWDHEATFLX','QNS','LDHEATFLX','LWDHEATFLX',
            'SDHEATFLX','NETUPWFLX','DSALTFLX','DAMPWFLX','MOC','u10','v10']:
    compute[var]=False
for var in ['MOD','VORT']:
    compute[var]=True

compute_vars={}
for var in ['MOD','VORT']:
    compute_vars[var]=['U','V']

#vars_palette={'SST':cmocean.cm.thermal,'SSS':cmocean.cm.haline,'T':cmocean.cm.thermal,'S':cmocean.cm.haline,'SSH':'tab20b','MLD':cmocean.cm.deep,
#              'MOD':cmocean.cm.ice_r,'VORT':f.home_made_cmap('on2'),'WINDSP':f.home_made_cmap('on3'),'bathy':cmocean.cm.deep} #'MOD':f.home_made_cmap('on3')
#for var in ['SSU','SSV','U','V','W','NETDHEATFLX','SWDHEATFLX','LWDHEATFLX','MOC']:
#    vars_palette[var]=cmocean.cm.balance
#for var in ['SICONC','SITHIC']:
#    vars_palette[var]=cmocean.cm.ice
#for var in ['NETUPWFLX','PRECIP']:
#    vars_palette[var]=cmocean.cm.rain

vars_unit = {'SST':'°C','SSS':'PSU','T':'°C','S':'PSU','SSH':'m','MLD':'m','SSU':'m/s','SSV':'m/s','U':'m/s','V':'m/s','W':'m/d','SICONC':'-',
             'SITHIC':'m','MOD':'m/s','VORT':'-','NETDHEATFLX':'W/m2','NETUPWFLX':'kg/m2/s','PRECIP':'kg/m2/s','WINDSP':'m/s','SWDHEATFLX':'W/m2',
             'LWDHEATFLX':'W/m2','bathy':'m','MOC':'Sverdrup'}

vars_longname = {'SST':'sea surface temperature','SSS':'sea surface salinity','T':'temperature','S':'salinity','SSH':'sea surface height',
                 'MLD':'mixed layer depth','SSU':'sea surface x-velocity','SSV':'sea surface y-velocity','U':'x-velocity','V':'y-velocity',
                 'W':'z-velocity','SICONC':'sea ice concentration','SITHIC':'sea ice thickness','MOD':'module de vitesse de courant de surface',
                 'VORT':'vorticite de surface relative','NETDHEATFLX':'Net Downward Heat Flux','NETUPWFLX':'Net Upward Water Flux',
                 'PRECIP':'Total precipitation','WINDSP':'wind speed module','SWDHEATFLX':'Shortwave Radiation',
                 'LWDHEATFLX':'Longwave Downward Heat Flux over open ocean','bathy':'Bathymetry','MOC':'Meridional Overturning Circulation'}

vars_vlims={}
vars_vlims['global']={'SSH':[-2,1],'SSU':[-1,1],'SSV':[-1,1],'SSS':[30,40],'SST':[-5,30],'MLD':[0,1000],'SICONC':[0,1],'SITHIC':[0,10],'MOD':[0,1.5],
                      'VORT':[-1,1],'NETDHEATFLX':[-500,500],'NETUPWFLX':[-0.0005,0.0005],'PRECIP':[0,0.002],'WINDSP':[0,25],'SWDHEATFLX':[-500,500],'LWDHEATFLX':[-500,500]}



