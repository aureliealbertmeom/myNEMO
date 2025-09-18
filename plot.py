import os
import glob
import re
import sys
import subprocess
import shutil
import numpy as np

#module gathering all the parameters, path etc
import lists as ls
#some functions
import functions as f

#Get the parameters for these new plots
dic_plot=f.read_single_yaml("current_plots.yml")

machine=dic_plot['machine']
exp=dic_plot['exp']
[config, simu]=exp.split('-')
variables=dic_plot['variables']
plot_types=dic_plot['plot_types']
plot_locs=dic_plot['plot_locs']
plot_regions=dic_plot['plot_regions']
frequency=dic_plot['frequency']
date_init=dic_plot['date_init']
date_end=dic_plot['date_end']


if "nemo_ref" in dic_exp:
    #We will use a reference simulation provided by NEMO
    nemo_ref_conf=dic_exp['nemo_ref']
    cppconf=nemo_ref_conf
    if 'add_key' in dic_exp:
        cppconf=cppconf+'_w'+dic_exp['add_key']
    if 'del_key' in dic_exp:
        cppconf=cppconf+'_wo'+dic_exp['del_key']
    print('We are going to run '+name+' on '+machine+' with '+xios_version_tag+' and '+nemo_version+' from reference NEMO case '+nemo_ref_conf)
else:
    #We will use another experiment as a reference, we need to specify the compilation parameters (compiler, xios version and cpp keys)
    cppconf=dic_exp['cpp_conf']
    print('We are going to run '+name+' on '+machine+' with '+xios_version_tag+' and '+nemo_version+' from previous run '+ref_exp)

#Specific path and tools relative to the machine
if machine in ls.all_machine:
    print(str(machine)+" it is !")
    path_dev=ls.all_path_dev[machine]
    path_mynemo=path_dev+'/myNEMO'
    path_work=ls.all_path_work[machine]
    path_scratch=ls.all_path_scratch[machine]
    path_store=ls.all_path_store[machine]
    print("The working path on "+str(machine)+" are :")
    print("  - dev : "+str(path_dev))
    print("  - work : "+str(path_work))
    print("  - scratch : "+str(path_scratch))
    print("  - store : "+str(path_store))
    jobsub=ls.all_jobsub_machine[machine]
else:
    sys.exit("Sorry, no other machines are parameterized yet")

#The compiler (intel, gnu, etc...)
compiler=dic_exp['compiler']
if compiler in ls.all_arch[machine]:
    print('We will use '+str(compiler))


#Decompose XIOS version
xios_version=xios_version_tag[4]
xios_tag=xios_version_tag[-4:]

#If XIOS version is already installed and compiled
if xios_version_tag in ls.all_tag_xios[machine]:
    path_xios=ls.all_path_xios[machine][xios_version_tag]
    print("Version "+str(xios_version_tag)+" has been compiled on "+str(machine)+" and is located at "+str(path_xios))

#A new version of XIOS for this machine has to be downloaded and compiled
else:
    path_xios=f.install_xios(machine, xios_version_tag, path_dev, path_mynemo,compiler)

#NEMO version

#Existing NEMO version on this machine
if nemo_version in ls.all_tag_nemo[machine]:
    path_nemo=ls.all_path_nemo[machine][nemo_version]
    print("Version "+str(nemo_version)+" has been downloaded on "+str(machine)+" and is located at "+str(path_nemo))
#Download a new version
else:
    path_nemo=f.download_nemo(nemo_version,machine,path_mynemo,path_dev)

#Existing compilation for this experiment
#comp_nemo here is a set of compilation parameter (intel, xios version and cpp keys) for which different geographical config can be run
comp_nemo=str(cppconf)+'_'+str(compiler)+'_'+str(xios_version_tag)
path_comp_nemo=path_nemo+'/cfgs/'+str(comp_nemo)

if comp_nemo in ls.all_comp_nemo[machine][nemo_version]:
    print('This specific reference NEMO config has already been compiled with the selected version of xios and compiler')
else:
    #Compilation of a ref case
    f.compile_nemo(compiler,xios_version_tag,path_nemo,path_mynemo,nemo_version,dic_exp,comp_nemo,cppconf,nemo_ref_conf,machine,path_xios)

#Set up the experiment : create directories
tmpdir_exp=path_scratch+'/TMPDIR_'+str(config)+'-'+str(new_exp)
sdir_exp_work=path_work+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-S'
rdir_exp_work=path_work+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-R'
sdir_exp_store=path_store+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-S'
rdir_exp_store=path_store+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-R'

if not os.path.exists(sdir_exp_work):
    print('Lets install this new experiment, we are creating new directories :')
    print('  - a TMPDIR : '+tmpdir_exp)
    print('  - a DIR for outputs: '+sdir_exp_work)
    print('  - a DIR for restarts: '+rdir_exp_work)
    print('  - a DIR for archiving outputs: '+sdir_exp_store)
    print('  - a DIR for archiving restarts: '+rdir_exp_store)
    os.makedirs(tmpdir_exp)
    os.makedirs(sdir_exp_work)
    os.makedirs(rdir_exp_work)
    os.makedirs(sdir_exp_store)
    os.makedirs(rdir_exp_store)
else:
    print('This is not a new experiment')
    if not os.path.exists(tmpdir_exp):
        print('The tmpdir does not exist anymore, we create it again')
        os.makedirs(tmpdir_exp)

#Get the path to the reference 
if jobnb > 1:
    print('This is not the first segment run for this experiment')
    ref_exp=name
    path_ref_exp=path_mynemo+'/NEMO/CONFIGS/'+ref_config+'/'+ref_exp
else:
    if 'ref_exp' in vars():
        print('The reference experiment is '+ref_exp)
        path_ref_exp=path_mynemo+'/NEMO/CONFIGS/'+ref_config+'/'+ref_exp
        if not os.path.exists(tmpdir_exp+'/nemo'):
            os.symlink(path_comp_nemo+'/BLD/bin/nemo.exe', tmpdir_exp+'/nemo')
    else:
        ref_exp='EXP00'
        print("The reference experiment is the default NEMO")
        path_ref_exp=path_nemo+'/cfgs/'+str(comp_nemo)+'/'+ref_exp

#We copy/link the namelists and other xml scripts
for filexp in os.listdir(path_ref_exp):
    if not os.path.exists(tmpdir_exp+'/'+filexp):
        if os.path.islink(path_ref_exp+'/'+filexp):
            sourcelink=os.path.realpath(path_ref_exp+'/'+filexp)
            os.symlink(sourcelink, tmpdir_exp+'/'+filexp)
        else:
            shutil.copyfile(path_ref_exp+'/'+filexp,tmpdir_exp+'/'+filexp)
            subprocess.call(["sed", "-i", "-e",  's/'+str(ref_exp)+'/'+str(name)+'/g', tmpdir_exp+'/'+filexp])

#We need to manage the segment of the exp (init or restart + time steps)
file_nam_temp=tmpdir_exp+'/template_namelist_cfg'
if nit0 == 1:
    if not os.path.exists(file_nam_temp):
        print("We start from init, we generate a template namelist to manage the following segments")
        shutil.copyfile(tmpdir_exp+'/namelist_cfg',file_nam_temp)
        print("Go modify the "+str(file_nam_temp)+" file, so that nn_it000, nn_itend, ln_rstart and rn_dt are filled with NIT000, NITEND, RESTART and RDT") 
        f.continue_question('If that is done, hit Continue to go on')
    else:
        print('We start from init, the template namelist '+file_nam_temp+' already exists, go check that it is ok')
        f.continue_question('If that is done, hit Continue to go on')

    print("We are using this freshly created template to generate the appropriate namelist for this segment")
    f.use_template(file_nam_temp,tmpdir_exp+'/namelist_cfg',{'NIT000':nit0,'NITEND':nitend,'RESTART':'false','RDT':dt})
else:
    print("We are continuing an existing exp, the template namelist should exist")
    if not os.path.exists(file_nam_temp):
        f.continue_question("No template namelist, create one and hit Continue to go on")
    print("We are using the template to generate the appropriate namelist for this segment")
    f.use_template(file_nam_temp,tmpdir_exp+'/namelist_cfg',{'NIT000':nit0,'NITEND':nitend,'RESTART':'true','RDT':dt})


#We need xios
if not os.path.exists(tmpdir_exp+'/xios'):
    os.symlink(path_xios+'/bin/xios_server.exe', tmpdir_exp+'/xios')


#Gather all necessary files
list_file=path_mynemo+'/NEMO/CONFIGS/list_files.yml'
path_input=path_work+'/'+str(config)+'/'+str(config)+'-I'

if "prev_exp" in dic_exp:
    print('This is not a reference run, the init files are gathered in -I and the forcing files are in DATA_FORCING')
    #Gather the init files
    all_init=f.find_exp_in_dics(list_file,name,'all_init',path_mynemo)
    f.gather_init(all_init,tmpdir_exp,path_input)
    #Gather the forcing files
    all_forc=f.find_exp_in_dics(list_file,name,'all_forc',path_mynemo)
    path_forc=f.find_exp_in_dics(list_file,name,'path_forc',path_mynemo)
    years=f.years_forc(nit0,nitend,dt,date_init)
    f.gather_forc(all_forc,tmpdir_exp,path_forc,years)
else:
    print('This is a reference run, all files are gathered in -I')
    all_files=f.find_exp_in_dics(list_file,name,'all_files',path_mynemo)
    f.gather_init(all_files,tmpdir_exp,path_input)

# Restarts or no restarts ?
core_nemo=dic_job['nemo_cores']
if nit0 == 1:
    print("We start from init, no restarts are needed")
else:
    f.process_restarts(nit0,tmpdir_exp,name,path_nemo,path_mynemo,compiler,xios_version_tag,core_nemo,jobsub,jobnb,rdir_exp_store,rdir_exp_work)

#Generate the job 

#Job parameters
node=dic_job['node']
core=dic_job['cores']
time=dic_job['time']
core_xios=dic_job['xios_cores']

f.setup_job(tmpdir_exp,jobnb,core_xios,path_mynemo,machine,node,core,time,name,core_nemo,config,sdir_exp_work,rdir_exp_work,nitend,jobsub)

print('If the job is successful, it will automatically launch extra job that will copy the outputs and restarts on work') 


