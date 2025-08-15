#Lists

all_machine=['irene']
all_jobsub_machine={}
all_jobsub_machine['irene']='ccc_msub'

all_path_dev={}
all_path_dev['irene']='/ccc/work/cont003/gen12020/alberaur/DEV'

all_path_work={}
all_path_work['irene']='/ccc/work/cont003/gen12020/alberaur'

all_path_scratch={}
all_path_scratch['irene']='/ccc/scratch/cont003/gen12020/alberaur'

all_path_store={}
all_path_store['irene']='/ccc/store/cont003/gen12020/alberaur'

all_arch={}
all_arch['irene']='X64_IRENE'

all_tag_xios={}
all_tag_xios['irene']=['XIOS3_2656','XIOS2_2430','XIOS3_2806']

all_path_xios={}
all_path_xios['irene']={}
all_path_xios['irene']['XIOS3_2806']=all_path_dev['irene']+'/xios3-trunk-2806'
all_path_xios['irene']['XIOS3_2656']=all_path_dev['irene']+'/xios3-trunk-2656'
all_path_xios['irene']['XIOS2_2430']=all_path_dev['irene']+'/xios-trunk-2430'

all_tag_nemo={}
all_tag_nemo['irene']=['NEMO_4.2.2','NEMO_5.0']

all_path_nemo={}
all_path_nemo['irene']={}
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

all_comp_nemo={}
all_comp_nemo['irene']={}
all_comp_nemo['irene']['NEMO_4.2.2']=['WED025_X64_IRENE_XIOS2_2430','X3_ORCA2_ICE_X64_IRENE_XIOS3_2656','WED025_X64_IRENE_XIOS2_2430']
all_comp_nemo['irene']['NEMO_5.0']=['X3_ORCA2_ICE_PISCES','X3_ORCA2_ICE_PISCES_X64_IRENE_XIOS3_2806','WED025_X64_IRENE_XIOS2_2430','WED025_X64_IRENE_XIOS3_2806']

all_exp_config_nemo={}
all_exp_config_nemo['irene']={}
all_exp_config_nemo['irene']['NEMO_4.2.2']={}
all_exp_config_nemo['irene']['NEMO_4.2.2']['WED025_X64_IRENE_XIOS2_2430']={}





