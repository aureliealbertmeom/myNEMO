import os
import re
import sys
import subprocess
import shutil

sys.path.append(os.path.realpath("."))
#module gathering all the parameters, path etc
import lists as ls
#some functions
import functions as f

machine='irene'
xios_version_tag='XIOS2_2430'
nemo_version='NEMO_4.2.2'
nemo_ref_conf='WED025'
config='WED025'
ref_exp='EXP00'
new_exp='EXP01'

match machine:
    case "irene":
        print(str(machine)+" it is !")
        path_dev=ls.all_path_dev[machine]
        path_work=ls.all_path_work[machine]
        path_scratch=ls.all_path_scratch[machine]
        path_store=ls.all_path_store[machine]
        print("The working path on "+str(machine)+" are :")
        print("  - dev : "+str(path_dev))
        print("  - work : "+str(path_work))
        print("  - scratch : "+str(path_scratch))
        print("  - store : "+str(path_store))
        arch_xios=ls.all_arch_xios[machine]
        arch_nemo=ls.all_arch_nemo[machine]
        print("We will use the "+str(arch_xios)+" arch file to compile XIOS on "+str(machine))
    case "else":
        sys.exit("Sorry, no other machines are parameterized yet")


#Decompose XIOS version
xios_version=xios_version_tag[4]
xios_tag=xios_version_tag[-3:]

#If XIOS version is already installed and compiled
if xios_version_tag in ls.all_tag_xios[machine]:
    path_xios=ls.all_path_xios[machine][xios_version_tag]
    print("Version "+str(xios_version_tag)+" has been compiled on "+str(machine)+" and is located at "+str(path_xios))

#A new version of XIOS for this machine has to be downloaded and compiled
else:
    print("We are going to compile XIOS on "+str(machine))
    scriptname=ls.all_path_dev[machine]+'/myNEMO/XIOS/get_xios'+str(xios_version)+'-'+str(xios_tag)+'.ksh'
    if not os.path.exists(scriptname):
                templatename=ls.all_path_dev[machine]+'/myNEMO/XIOS/template_get_xios_tag.ksh'
                f.use_template(templatename, scriptname, {'VERS':str(xios_version),'TAG':str(xios_tag)})
    print('Then use the get_xios'+str(xios_version)+'-'+str(xios_tag)+'.sh script located in the subrepo XIOS to download XIOS')

    #A script with the proper arch to compile on this machine
    scriptname=ls.all_path_dev[machine]+'myNEMO/XIOS/compile_xios_'+str(arch_xios)+'.sh'
    #check if the corresponding compile_xios script already exists
    if not os.path.exists(scriptname):
                templatename=ls.all_path_dev[machine]+'myNEMO/XIOS/template_compile_xios_arch.sh'
                f.use_template(templatename, scriptname, {'ARCH':str(arch_xios)})
    print("Now you just have to compile XIOS using the compile_xios_"+str(arch_xios)+".sh script that is available in XIOS subdirectory") 

    #The path depends on the version AND tag    
    path_xios=ls.all_path_dev[machine]+'/xios'+str(xios_version)+'-trunk-'+str(xios_tag)

#NEMO version

#Existing NEMO version on this machine
if nemo_version in ls.all_tag_nemo[machine]:
    path_nemo=ls.all_path_nemo[machine][nemo_version]
    print("Version "+str(nemo_version)+" has been downloaded on "+str(machine)+" and is located at "+str(path_nemo))
#Download a new version
else:
    print("We are going to download NEMO version "+str(nemo_version)+" on "+str(machine))
    scriptname=ls.all_path_dev[machine]+'myNEMO/NEMO/get_nemo_'+str(nemo_version)+'.sh'
    if not os.path.exists(scriptname):
        templatename=ls.all_path_dev[machine]+'myNEMO/NEMO/get_nemo_tag.sh'
        f.use_template(templatename, scriptname, {'TAG':str(nemo_version)})
    print('Use the '+str(scriptname)+' script to download '+str(nemo_version))

#Existing compilation for this experiment
#comp_nemo here is a set of compilation parameter (intel, xios version and cpp keys) for which different geographical config can be run
comp_nemo=str(nemo_ref_conf)+'_'+str(arch_nemo)+'_'+str(xios_version_tag)
path_comp_nemo=ls.all_path_dev[machine]+'/'+str(nemo_version)+'/cfgs/'+str(comp_nemo)

if not os.path.exists(path_comp_nemo):
    #Compilation of a ref case
    print('Now we are going to compile the selected version of NEMO with the previously selected version of XIOS')
    #Looking for the proper arch file + adding the xios version in it
    archname=ls.all_path_dev[machine]+'/myNEMO/NEMO/arch/arch-'+str(arch_nemo)+'_'+str(xios_version_tag)+'.fcm'
    if not os.path.exists(archname):
        templatename=ls.all_path_dev[machine]+'myNEMO/NEMO/arch/template_arch-'+str(arch_nemo)+'_xios_path.fcm'
        f.use_template(templatename, scriptname, {'PATH_XIOS':str(path_xios)})
    print('Copy the '+str(archname)+' arch file to '+str(path_dev)+'/'+str(nemo_version)+'/arch/CNRS')

    #A script to compile the reference config with proper arch file
    scriptname=ls.all_path_dev[machine]+'/myNEMO/NEMO/compile_nemo_'+str(comp_nemo)+'.ksh'
    if not os.path.exists(scriptname):
        templatename=ls.all_path_dev[machine]+'/myNEMO/NEMO/template_compile_config_ref_arch.ksh'
        f.use_template(templatename, scriptname, {'ARCH':str(arch_nemo)+'_'+str(xios_version_tag),'REFCONF':str(nemo_ref_conf)})
    print('Copy and use the script '+str(scriptname)+'  NEMO to '+str(path_dev)+'/'+str(nemo_version)+' to compile the '+str(nemo_ref_conf)+' reference with selected version of XIOS ')
else:
    print('This specific reference NEMO config has already been compiled with the selected version of xios and compiler')
    print('We are going to archive this new comp_nemo by keeping its ccp keys file and MY_SRC files if there are any')
    path_comp_nemo_nemo=ls.all_path_dev[machine]+'/'+str(nemo_version)+'/cfgs/'+str(comp_nemo)
    path_comp_nemo_my=ls.all_path_dev[machine]+'/myNEMO/NEMO/'+str(nemo_version)+'/'+str(comp_nemo)
    os.makedirs(path_comp_nemo_my)
    cppname='cpp_'+str(comp_nemo)+'.fcm'
    shutil.copyfile(path_comp_nemo_nemo+'/'+cppname,path_comp_nemo_my+'/'+cppname)
    if len(os.listdir(path_comp_nemo_nemo+'/MY_SRC')) > 0:
        os.makedirs(path_comp_nemo_my+'/MY_SRC')
        for filemy in os.listdir(path_comp_nemo_nemo+'/MY_SRC'):
            shutil.copyfile(path_comp_nemo_nemo+'/MY_SRC/'+filemy,path_comp_nemo_my+'/MY_SRC/'+filemy)
    print('You can now update the list of comp_nemos for '+str(nemo_version)+' on '+str(machine))
else:
    print('This specific reference NEMO config has already been compiled with the selected version of xios and compiler')


#New experiment
print('Lets install this new experiment :')
tmpdir_exp=path_scratch+'/TMPDIR_'+str(config)+'-'+str(new_exp)
sdir_exp_work=path_work+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-S'
rdir_exp_work=path_work+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-R'
sdir_exp_store=path_store+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-S'
rdir_exp_store=path_store+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-R'

os.makedirs(tmpdir_exp)
os.makedirs(sdir_exp_work)
os.makedirs(rdir_exp_work)
os.makedirs(sdir_exp_store)
os.makedirs(rdir_exp_store)
print('Path to a tmpdir, some dirs for outputs and restarts both on work and store have been created')

if ref_exp == 'EXP00':
    print('The reference experiment is the default NEMO EXP00')
    path_exp00=path_comp_nemo+'/EXP00'
    for filexp in os.listdir(path_exp00):
        if os.path.islink(path_exp00+'/'+filexp):
            sourcelink=os.readlink(path_exp00+'/'+filexp)
            os.symlink(sourcelink, tmpdir_exp+'/'+filexp)
        else:
            shutil.copyfile(path_exp00+'/'+filexp,tmpdir_exp+'/'+filexp)

#We need xios
os.symlink(path_xios+'/bin/xios_server.exe', tmpdir_exp+'/xios_server.exe')




                






