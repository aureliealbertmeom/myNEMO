import os
import re
import sys
import subprocess
import shutil
import numpy as np

#module gathering all the parameters, path etc
import lists as ls
#some functions
import functions as f

#Get the parameters for this new experiment
dic_exp=f.read_single_yaml("current_experiment.yml")

machine=dic_exp['machine']
xios_version_tag=dic_exp['xios']
nemo_version=dic_exp['nemo']
name=dic_exp['name']
[config, new_exp]=name.split('-')
ref_exp=dic_exp['prev_exp']
nit0=dic_exp['nit0']
nitend=dic_exp['nitend']

if "nemo_ref" in dic_exp:
    #We will use a reference simulation provided by NEMO
    nemo_ref_conf=dic_exp['nemo_ref']
    cppconf=nemo_ref_conf
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
    print("We are going to compile XIOS on "+str(machine))
    scriptname=path_mynemo+'/XIOS/get_xios_'+str(xios_version_tag)+'.ksh'
    if not os.path.exists(scriptname):
        templatename=path_mynemo+'/XIOS/template_get_xios_tag.ksh'
        f.use_template(templatename, scriptname, {'VERS':str(xios_version),'TAG':str(xios_tag)})
    subprocess.call(["chmod", "+x",scriptname])
    print('Use the script '+str(scriptname)+'.sh script to download '+xios_version_tag+' in '+path_dev)
    f.continue_question('Hit Continue to go on')
    path_xios=path_dev+'/xios'+xios_version+'-trunk-'+xios_tag
    #A script with the proper arch to compile on this machine
    scriptname=path_mynemo+'/XIOS/compile_xios_'+str(compiler)+'.sh'
    #check if the corresponding compile_xios script already exists
    if not os.path.exists(scriptname):
        templatename=path_mynemo+'/XIOS/template_compile_xios_arch.ksh'
        f.use_template(templatename, scriptname, {'ARCH':str(compiler)})

    shutil.copyfile(scriptname,path_xios+'/compile_xios_'+str(compiler)+'.sh')
    subprocess.call(["chmod", "+x", path_xios+'/compile_xios_'+str(compiler)+'.sh'])
    print('Compile XIOS using script compile_xios_'+str(compiler)+'.sh in '+path_xios) 
    f.continue_question('If succesfully compiled, Hit Continue to go on')
    print('Add '+xios_version+' to the list all_path_xios for '+machine+' and '+path_xios+' to all_path_xios')

#NEMO version

#Existing NEMO version on this machine
if nemo_version in ls.all_tag_nemo[machine]:
    path_nemo=ls.all_path_nemo[machine][nemo_version]
    print("Version "+str(nemo_version)+" has been downloaded on "+str(machine)+" and is located at "+str(path_nemo))
#Download a new version
else:
    print("We are going to download NEMO version "+str(nemo_version)+" on "+str(machine))
    scriptname=path_mynemo+'/NEMO/get_nemo_'+str(nemo_version)+'.sh'
    if not os.path.exists(scriptname):
        templatename=path_mynemo+'/NEMO/get_nemo_tag.sh'
        f.use_template(templatename, scriptname, {'TAG':str(nemo_version)})
    print('Use the '+str(scriptname)+' script to download '+str(nemo_version))

#Existing compilation for this experiment
#comp_nemo here is a set of compilation parameter (intel, xios version and cpp keys) for which different geographical config can be run
comp_nemo=str(cppconf)+'_'+str(compiler)+'_'+str(xios_version_tag)
path_comp_nemo=path_nemo+'/cfgs/'+str(comp_nemo)

if comp_nemo in ls.all_comp_nemo[machine][nemo_version]:
    print('This specific reference NEMO config has already been compiled with the selected version of xios and compiler')
else:
    #Compilation of a ref case
    print('Now we are going to compile the selected version of NEMO with the previously selected version of XIOS')
    #Looking for the proper arch file + adding the xios version in it
    archname='arch-'+str(compiler)+'_'+str(xios_version_tag)+'.fcm'
    if not os.path.exists(path_nemo+'/arch/CNRS/'+archname):
        if not os.path.exists(path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname):
            templatename=path_mynemo+'/NEMO/'+nemo_version+'/arch/template_arch-'+str(compiler)+'_xios_path.fcm'
            f.use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname, {'PATH_XIOS':str(path_xios)})
        print('We copy the '+str(archname)+' arch file to '+path_nemo+'/arch/CNRS')
        shutil.copyfile(path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname,path_nemo+'/arch/CNRS/'+archname)

    #A script to compile the reference config with proper arch file
    scriptname='compile_nemo_'+str(comp_nemo)+'.ksh'
    if not os.path.exists(path_nemo+'/'+scriptname):
        if not os.path.exists(path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname):
            if 'del_key' in dic_exp:
                del_key=dic_exp['del_key']
                templatename=path_mynemo+'/NEMO/template_compile_config_ref_arch_delkey.ksh'
                f.use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname, {'ARCH':str(compiler)+'_'+str(xios_version_tag),'REFCONF':str(cppconf),'KEYDEL':str(del_key)})
            elif 'add_key' in dic_exp:
                add_key=dic_exp['add_key']
                templatename=path_mynemo+'/NEMO/template_compile_config_ref_arch_addkey.ksh'
                f.use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname, {'ARCH':str(compiler)+'_'+str(xios_version_tag),'REFCONF':str(cppconf),'KEYADD':str(add_key)})
            else:
                templatename=path_mynemo+'/NEMO/template_compile_config_ref_arch.ksh'
                f.use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname, {'ARCH':str(compiler)+'_'+str(xios_version_tag),'REFCONF':str(cppconf)})
    shutil.copyfile(path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname,path_nemo+'/'+scriptname)
    subprocess.call(["chmod", "+x", path_nemo+'/'+scriptname])
    print('You need to run '+str(scriptname)+' at '+path_nemo+' to compile the '+str(cppconf)+' reference with selected version of XIOS')
    f.continue_question('Hit Continue when it is done')

    print('We are going to archive this new comp_nemo by keeping its ccp keys file and MY_SRC files if there are any')
    path_comp_nemo_nemo=path_nemo+'/cfgs/'+str(comp_nemo)
    path_comp_nemo_my=path_mynemo+'/NEMO/'+str(nemo_version)+'/cfgs/'+str(comp_nemo)
    os.makedirs(path_comp_nemo_my)
    cppname='cpp_'+str(comp_nemo)+'.fcm'
    shutil.copyfile(path_comp_nemo_nemo+'/'+cppname,path_comp_nemo_my+'/'+cppname)
    if len(os.listdir(path_comp_nemo_nemo+'/MY_SRC')) > 0:
        os.makedirs(path_comp_nemo_my+'/MY_SRC')
        for filemy in os.listdir(path_comp_nemo_nemo+'/MY_SRC'):
            shutil.copyfile(path_comp_nemo_nemo+'/MY_SRC/'+filemy,path_comp_nemo_my+'/MY_SRC/'+filemy)
    print('You can now update the list of all_comp_nemo for '+str(nemo_version)+' on '+str(machine)+' by adding '+str(comp_nemo))
    f.continue_question('Hit Continue when it is done')


#Set up the experiment
tmpdir_exp=path_scratch+'/TMPDIR_'+str(config)+'-'+str(new_exp)
sdir_exp_work=path_work+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-S'
rdir_exp_work=path_work+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-R'
sdir_exp_store=path_store+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-S'
rdir_exp_store=path_store+'/'+str(config)+'/'+str(config)+'-'+str(new_exp)+'-R'

if not os.path.exists(sdir_exp_work):
    print('Lets install this new experiment :')
    os.makedirs(tmpdir_exp)
    os.makedirs(sdir_exp_work)
    os.makedirs(rdir_exp_work)
    os.makedirs(sdir_exp_store)
    os.makedirs(rdir_exp_store)
    print('Path to a tmpdir, some dirs for outputs and restarts both on work and store have been created')
else:
    print('This is not a new experiment')
    if not os.path.exists(tmpdir_exp):
        print('The tmpdir does not exist anymore, we create it again')
        os.makedirs(tmpdir_exp)

#Get the path to the reference and copy/link the files+nemo executable
if 'nemo_ref_conf' in vars():
    print("The reference experiment is the default NEMO")
    path_ref_exp=path_nemo+'/cfgs/'+str(comp_nemo)+'/'+ref_exp
else:
    print('The reference experiment is '+ref_exp)
    path_ref_exp=path_mynemo+'/NEMO/CONFIGS/'+config+'/'+config+'-'+ref_exp
    if not os.path.exists(tmpdir_exp+'/nemo'):
        os.symlink(path_comp_nemo+'/BLD/bin/nemo.exe', tmpdir_exp+'/nemo')

for filexp in os.listdir(path_ref_exp):
    if not os.path.exists(tmpdir_exp+'/'+filexp):
        if os.path.islink(path_ref_exp+'/'+filexp):
            sourcelink=os.path.realpath(path_ref_exp+'/'+filexp)
            os.symlink(sourcelink, tmpdir_exp+'/'+filexp)
        else:
            shutil.copyfile(path_ref_exp+'/'+filexp,tmpdir_exp+'/'+filexp)
            subprocess.call(["sed", "-i", "-e",  's/'+str(ref_exp)+'/'+str(new_exp)+'/g', tmpdir_exp+'/'+filexp])

#We need xios
if not os.path.exists(tmpdir_exp+'/xios'):
    os.symlink(path_xios+'/bin/xios_server.exe', tmpdir_exp+'/xios')

#Gather the forcing files and job options
list_file=path_mynemo+'/NEMO/CONFIGS/list_files.yml'
alldics=f.read_multiple_yaml(list_file)
for dic in np.arange(len(alldics)):
    if alldics[dic]['name'] == config+'-'+new_exp:
        all_files=alldics[dic]['all_files']
        [node,core,time,core_xios,core_nemo]=alldics[dic]['job']


if 'all_files' in vars():
    for filefrc in all_files:
        if not os.path.exists(tmpdir_exp+'/'+filefrc):
            path_input=path_work+'/'+str(config)+'/'+str(config)+'-I'
            os.symlink(path_input+'/'+filefrc, tmpdir_exp+'/'+filefrc)
else:
    print('The list of forcing files is not available for this reference experiment, fill out '+path_mynemo+'/NEMO/CONFIGS/list_files.yml')
    f.continue_question('And hit Continue to proceed')
    #2nd chance to get the list of forcing files
    list_file=path_mynemo+'/NEMO/CONFIGS/list_files.yml'
    alldics=f.read_multiple_yaml(list_file)
    for dic in np.arange(len(alldics)):
        if alldics[dic]['name'] == config+'-'+new_exp:
            all_files=alldics[dic]['all_files']
            [node,core,time,core_xios,core_nemo]=alldics[dic]['job']
    for filefrc in all_files:
        if not os.path.exists(tmpdir_exp+'/'+filefrc):
            path_input=path_work+'/'+str(config)+'/'+str(config)+'-I'
            os.symlink(path_input+'/'+filefrc, tmpdir_exp+'/'+filefrc)

#Generate the job 
jobname=tmpdir_exp+'/job.ksh'
if not os.path.exists(jobname):
    if int(core_xios) > 0:
        jobtemplate=path_mynemo+'/NEMO/job_multi_'+machine+'.ksh'
        f.use_template(jobtemplate, jobname, {'NODE':node,'CORE':core,'TIME':time,'TMPDIR':str(tmpdir_exp),'CONFEXP':path_mynemo+'/NEMO/CONFIGS/'+name})
        subprocess.call(["chmod", "+x", jobname])
        mpmdname=tmpdir_exp+'/mpmd.conf'
        if not os.path.exists(mpmdname):
            mpmdtemplate=path_mynemo+'/NEMO/template_mpmd.conf'
            core_xiosm1=int(core_xios)-1
            cores_m1=int(core)-1
            if int(core_xios)+int(core_nemo) != int(core):
                sys.exit('Wrong repartition of cores etween nemo and xios')
            else:
                f.use_template(mpmdtemplate, mpmdname, {'XIOS':str(core_xiosm1),'NEMO1':core_xios,'NEMO2':coresm1})
                subprocess.call(["chmod", "+x", mpmdname])
    else:
        jobtemplate=path_mynemo+'/NEMO/job_'+machine+'.ksh'
        f.use_template(jobtemplate, jobname, {'NODE':node,'CORE':core,'TIME':time,'TMPDIR':str(tmpdir_exp),'CONFEXP':path_mynemo+'/NEMO/CONFIGS/'+name})
        subprocess.call(["chmod", "+x", jobname])


#We also set up the output and restart job before launching
joboname=tmpdir_exp+'/job_output.ksh'
if not os.path.exists(joboname):
    jobotemplate=path_mynemo+'/NEMO/job_output_'+machine+'.ksh'
    f.use_template(jobotemplate, joboname, {'TMPDIR':tmpdir_exp,'CONFCASE':name,'SDIR':sdir_exp_work})
    subprocess.call(["chmod", "+x", joboname])

jobrname=tmpdir_exp+'/job_restart.ksh'
if not os.path.exists(jobrname):
    jobrtemplate=path_mynemo+'/NEMO/job_restart_'+machine+'.ksh'
    f.use_template(jobrtemplate, jobrname, {'TMPDIR':tmpdir_exp,'CONFCASE':name,'NITEND':nitend,'RDIR':rdir_exp_work})
    subprocess.call(["chmod", "+x", jobrname])


#Launch the main job
runname=tmpdir_exp+'/run.ksh'
if not os.path.exists(runname):
    runtemplate=path_mynemo+'/NEMO/run_'+machine+'.ksh'
    f.use_template(runtemplate, runname, {'SUB':jobsub,'TMPDIR':str(tmpdir_exp)})
    subprocess.call(["chmod", "+x", runname])

f.continue_question('We are about to launch the job in '+tmpdir_exp+' check that everything is ok and hit Continue to proceed')
subprocess.run(runname,shell=True)

print('You can check the progress of your job with qmt command and the progression of NEMO with tail -f ocean.output and tts')

#If successful add this experiment to the list and save output files and restarts in the appropriate dirs
print('If the job is successful, it will automatically launch extra job that will copy the outputs and restarts on work') 


