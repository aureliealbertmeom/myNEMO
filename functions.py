#! /usr/bin/env python
import os
import glob
import sys
import shutil
import subprocess
import inquirer
import yaml
import numpy as np

def use_template(tempname, scriptname, dict_strings_values):
    """
    Copy a template script and replace a list of strings by chosen arguments in it
    Parameters :
     - name of the template script
     - name of the resulting script
     - a dictionary that match default string and the corresponding value we want to replace it
    Returns :
    None
    """
    shutil.copyfile(tempname,scriptname)
    for string in dict_strings_values:
        subprocess.call(["sed", "-i", "-e",  's%'+str(string)+'%'+str(dict_strings_values[string])+'%g',scriptname])

def continue_question(message):
    """
    use inquirer to ask the user if they want to go on after completing a task
    Parameters :
      - message :  string that will be printed to the user
    """
    q="continue"
    question = [ inquirer.List(q,message=message+" hit Continue", choices=["Continue","Stop"]) ]
    answer = inquirer.prompt(question)
    continue_bool=answer[q]

    match continue_bool:
        case "Stop":
            sys.exit("Exiting, bye")

def open_question(message):
    """
    Ask an open question to the user and retrieve their answer
    """
    qx="question"
    questionx = [ inquirer.Text(qx,message=message) ]
    answerx = inquirer.prompt(questionx)
    return answerx[qx]

def read_single_yaml(filei):
    """
    Read a yaml file and returns a dictionary
    Parameters :
      - filei : path to the yaml file containing one dic (string)
    """
    with open(filei) as stream:
        dic=yaml.safe_load(stream)

    return dic[0]

def read_multiple_yaml(filei):
    """
    Read a yaml file and returns a list of dictionaries
    Parameters :
      - filei : path to the yaml file containing one dic (string)
    """
    with open(filei) as stream:
        dic=yaml.safe_load(stream)

    return dic

def install_xios(machine, xios_version_tag, path_dev, path_mynemo,compiler):
    """
    Install the xios_version_tag version of XIOS on the machine
    using script from myNEMO
    """
    print("We are going to compile XIOS on "+str(machine))
    scriptname='get_xios_'+str(xios_version_tag)+'.ksh'
    #Separate version tag in version and tag
    xios_version=xios_version_tag[4]
    xios_tag=xios_version_tag[-4:]
    
    if not os.path.exists(path_dev+'/'+scriptname):
        if not os.path.exists(path_mynemo+'/XIOS/'+scriptname):
            templatename=path_mynemo+'/XIOS/template_get_xios_tag.ksh'
            use_template(templatename, path_mynemo+'/XIOS/'+scriptname, {'VERS':str(xios_version),'TAG':str(xios_tag)})
            subprocess.call(["chmod", "+x",path_mynemo+'/XIOS/'+scriptname])
        shutil.copyfile(path_mynemo+'/XIOS/'+scriptname,path_dev+'/'+scriptname)
    print('Go to '+path_dev+' and use the script '+str(scriptname)+'.ksh script to download '+xios_version_tag)
    continue_question('If successfully downloaded,')
    path_xios=path_dev+'/xios'+xios_version+'-trunk-'+xios_tag
    #A script with the proper arch to compile on this machine
    scriptname='compile_xios_'+str(compiler)+'.ksh'
    #check if the corresponding compile_xios script already exists
    if not os.path.exists(path_mynemo+'/XIOS/'+scriptname):
        templatename=path_mynemo+'/XIOS/template_compile_xios_arch.ksh'
        use_template(templatename, path_mynemo+'/XIOS/'+scriptname, {'ARCH':str(compiler)})
        subprocess.call(["chmod", "+x", path_mynemo+'/XIOS/'+scriptname])
    shutil.copyfile(path_mynemo+'/XIOS/'+scriptname,path_xios+'/'+scriptname)
    print('Go to '+path_xios+' and compile XIOS using script '+scriptname)
    continue_question('If succesfully compiled,')
    print('Go to '+path_mynemo+' and modify lists.py : add '+xios_version_tag+' to the list all_tag_xios for '+machine+' and '+path_xios+' to all_path_xios')
    continue_question('If that is done,')
    return path_xios

def download_nemo(nemo_version,machine,path_mynemo,path_dev):
    """
    Download the nemo_version of NEMO on the machine
    """
    print("We are going to download NEMO version "+str(nemo_version)+" on "+str(machine))
    [nemo,tag]=nemo_version.split('_')
    scriptname=path_mynemo+'/NEMO/get_nemo_'+str(tag)+'.ksh'
    if not os.path.exists(scriptname):
        templatename=path_mynemo+'/NEMO/template_get_nemo_tag.ksh'
        use_template(templatename, scriptname, {'TAG':str(tag),'PATH':path_dev})
    shutil.copyfile(scriptname,path_dev+'/get_nemo_'+str(tag)+'.ksh')
    subprocess.call(["chmod", "+x", path_dev+'/get_nemo_'+str(tag)+'.ksh'])
    print('Go to '+path_dev+' and download NEMO using script get_nemo_'+str(tag)+'.ksh')
    continue_question('If succesfully dowloaded,')
    path_nemo=path_dev+'/'+nemo_version
    print('Go to '+path_mynemo+' and modify lists.py : add '+nemo_version+' to the list all_tag_nemo for '+machine+' and '+path_nemo+' to all_path_nemo')
    continue_question('If that is done,')
    return path_nemo

def compile_nemo(compiler,xios_version_tag,path_nemo,path_mynemo,nemo_version,dic_exp,comp_nemo,cppconf,nemo_ref_conf,machine,path_xios):
    """
    Compile the nemo_version of NEMO with the xios_version of xios and compiler on machine
    """
    print('Now we are going to compile the selected version of NEMO with the previously selected version of XIOS')
    #Looking for the proper arch file + adding the xios version in it
    archname='arch-'+str(compiler)+'_'+str(xios_version_tag)+'.fcm'
    if not os.path.exists(path_nemo+'/arch/CNRS/'+archname):
        if not os.path.exists(path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname):
            templatename=path_mynemo+'/NEMO/'+nemo_version+'/arch/template_arch-'+str(compiler)+'_xios_path.fcm'
            if not os.path.exists(templatename):
                print('Got to '+path_nemo+'/NEMO/'+nemo_version+'/arch/ and make sure there is a template arch called template_arch-'+str(compiler)+'_xios_path.fcm')
                continue_question('When it is done,')
            use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname, {'PATH_XIOS':str(path_xios)})
        print('We copy the '+str(archname)+' arch file to '+path_nemo+'/arch/CNRS')
        shutil.copyfile(path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname,path_nemo+'/arch/CNRS/'+archname)

    #A script to compile the reference config with proper arch file
    scriptname='compile_nemo_'+str(comp_nemo)+'.ksh'
    if not os.path.exists(path_nemo+'/'+scriptname):
        if not os.path.exists(path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname):
            if 'del_key' in dic_exp:
                del_key=dic_exp['del_key']
                templatename=path_mynemo+'/NEMO/template_compile_config_ref_arch_delkey.ksh'
                use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname, {'ARCH':str(compiler)+'_'+str(xios_version_tag),'REFCONF':str(nemo_ref_conf),'CPPCONF':str(comp_nemo),'KEYDEL':str(del_key)})
            elif 'add_key' in dic_exp:
                add_key=dic_exp['add_key']
                templatename=path_mynemo+'/NEMO/template_compile_config_ref_arch_addkey.ksh'
                use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname, {'ARCH':str(compiler)+'_'+str(xios_version_tag),'REFCONF':str(nemo_ref_conf),'CPPCONF':str(comp_nemo),'KEYADD':str(add_key)})
            else:
                templatename=path_mynemo+'/NEMO/template_compile_config_ref_arch.ksh'
                use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname, {'ARCH':str(compiler)+'_'+str(xios_version_tag),'REFCONF':str(nemo_ref_conf),'CPPCONF':str(comp_nemo)})
    shutil.copyfile(path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname,path_nemo+'/'+scriptname)
    subprocess.call(["chmod", "+x", path_nemo+'/'+scriptname])
    print('Go to '+path_nemo+' and compile NEMO with '+str(scriptname))
    continue_question('If successfully compiled,')

    #Archiving scripts
    print('We are going to archive this new comp_nemo by keeping its ccp keys file and MY_SRC files if there are any')
    path_comp_nemo_nemo=path_nemo+'/cfgs/'+str(comp_nemo)
    path_comp_nemo_my=path_mynemo+'/NEMO/'+str(nemo_version)+'/cfgs/'+str(comp_nemo)
    if not os.path.exists(path_comp_nemo_my):
        os.makedirs(path_comp_nemo_my)
    cppname='cpp_'+str(comp_nemo)+'.fcm'
    shutil.copyfile(path_comp_nemo_nemo+'/'+cppname,path_comp_nemo_my+'/'+cppname)
    if len(os.listdir(path_comp_nemo_nemo+'/MY_SRC')) > 0:
        os.makedirs(path_comp_nemo_my+'/MY_SRC')
        for filemy in os.listdir(path_comp_nemo_nemo+'/MY_SRC'):
            shutil.copyfile(path_comp_nemo_nemo+'/MY_SRC/'+filemy,path_comp_nemo_my+'/MY_SRC/'+filemy)
    print('Go to '+path_mynemo+' and modify lists.py : add '+comp_nemo+' to all_comp_nemo for '+str(nemo_version)+' on '+str(machine))
    continue_question('If that is done,')

def find_exp_in_dics(list_file,name,prop,path_mynemo):
    """
    Check if name exists in list_file and retrieve prop from the dic
    """
    
    alldics=read_multiple_yaml(list_file)
    for dic in np.arange(len(alldics)):
        if alldics[dic]['name'] == name:
            all_files=alldics[dic][prop]

    if 'all_files' not in vars():
        print('The list of forcing files is not available for this reference experiment, fill out '+path_mynemo+'/NEMO/CONFIGS/list_files.yml')
        continue_question('When it is done,')

    alldics=read_multiple_yaml(list_file)
    for dic in np.arange(len(alldics)):
        if alldics[dic]['name'] == name:
            all_files=alldics[dic][prop]

    if 'all_files' not in vars():
        sys.exit('The list of forcing files is still not available for this reference experiment, relaunch start so it actualizes')

    
    return all_files

def process_restarts(nit0,tmpdir_exp,name,path_nemo,path_mynemo,compiler,xios_version_tag,core_nemo,jobsub,jobnb,rdir_exp_store,rdir_exp_work):
    """
    Look for appropriate restart in tmpdir_exp and recombine and compile rebuild_nemo if needed
    """
    print("We are continuing an existing exp, we need restarts")
    nitm1=int(nit0)-1
    nitm18="{:08d}".format(nitm1)
    #Check for restart.nc
    if os.path.exists(tmpdir_exp+'/restart.nc'):
        #Check if correct restart
        sourcelink=os.path.realpath(tmpdir_exp+'/restart.nc')
        if sourcelink != tmpdir_exp+'/'+name+'_'+str(nitm18)+'_restart.nc':
            print('Wrong restart, we need modify it')
            linkrst_bool=True
        else:
            linkrst_bool=False
    else:
        linkrst_bool=True
        #Check for restart.nc with recombined restarts
        if not os.path.exists(tmpdir_exp+'/'+name+'_'+str(nitm18)+'_restart.nc'):
            #Check for subdomain restarts
            if len(glob.glob(tmpdir_exp+'/'+name+'_*'+str(nitm1)+'_restart*nc')) == 0:
                print('There are no restart files in '+tmpdir_exp+', we will check the -R directory')
                if (len(glob.glob(rdir_exp_work+'/'+name+'_*'+str(nitm1)+'_restart*'))+len(glob.glob(rdir_exp_store+'/'+name+'_*'+str(nitm1)+'_restart*'))) > 0:
                    print('Lets bring them back to tmpdir')
                    if len(glob.glob(rdir_exp_work+'/'+name+'_*'+str(nitm1)+'_restart*')) > 0:
                        for filerst in glob.glob(rdir_exp_work+'/'+name+'_*'+str(nitm1)+'_restart*'):
                            basename=os.path.basename(filerst)
                            shutil.copyfile(filerst,tmpdir_exp+'/'+basename)
                    else:
                        for filerst in glob.glob(rdir_exp_store+'/'+name+'_*'+str(nitm1)+'_restart*'):
                            basename=os.path.basename(filerst)
                            shutil.copyfile(filerst,tmpdir_exp+'/'+basename)
                    subprocess.call(["tar", "-xvf", tmpdir_exp+'/'+basename])
                else:
                    sys.exit('No restarts have been found at all, we have to stop')
            print("We need to recombine restarts")
            #Looking for rebuild_nemo tool
            if not os.path.exists(path_nemo+'/tools/REBUILD_NEMO/rebuild_nemo'):
                print("We need to compile the rebuild tool")
                compilerebuild=path_nemo+'/tools/compile_rebuild_'+compiler+'.ksh'
                templatename=path_mynemo+'/NEMO/template_compile_tool.ksh'
                use_template(templatename, compilerebuild, {'ARCH':str(compiler)+'_'+str(xios_version_tag),'TOOL':'REBUILD_NEMO','PATH':path_nemo+'/tools'})
                subprocess.call(["chmod", "+x", compilerebuild])
                continue_question('We are about to compile REBUILD_NEMO in '+path_nemo+'/tools/ check that everything is ok,')
                subprocess.run(compilerebuild,shell=True)
                continue_question('If compilation went ok,')
                shutil.copyfile(compilerebuild,path_mynemo+'/NEMO/compile_rebuild_'+compiler+'_'+str(xios_version_tag)+'.ksh')
            scriptrebuirst=tmpdir_exp+'/job_rebuild_restart'+str(jobnb)+'.ksh'
            templatename=path_mynemo+'/NEMO/job_rebuild_restart_irene.ksh'
            use_template(templatename, scriptrebuirst, {'TMPDIR':tmpdir_exp,'PATH_REBUILD':path_nemo+'/tools/REBUILD_NEMO','BASE':name+'_'+str(nitm18)+'_restart','DOMAINS':core_nemo})
            subprocess.call(["chmod", "+x",scriptrebuirst])
            continue_question('We are about to recombine restarts,')
            subprocess.call([jobsub,scriptrebuirst])
            continue_question('The restarts are being recombined, when it is done,')

    #Recombined restart exists
    if linkrst_bool == True:
        os.symlink(tmpdir_exp+'/'+name+'_'+str(nitm18)+'_restart.nc',tmpdir_exp+'/restart.nc')
        if os.path.exists(tmpdir_exp+'/'+name+'_'+str(nitm18)+'_restart_ice.nc'):
            os.symlink(tmpdir_exp+'/'+name+'_'+str(nitm18)+'_restart_ice.nc',tmpdir_exp+'/restart_ice.nc')


def setup_job(tmpdir_exp,jobnb,core_xios,path_mynemo,machine,node,core,time,name,core_nemo,config,sdir_exp_work,rdir_exp_work,nitend,jobsub):
    """
    Set up all the scripts needed to run the segment of the simulation
    """
    jobname=tmpdir_exp+'/job'+str(jobnb)+'.ksh'
    if int(core_xios) > 0:
        if not os.path.exists(jobname):
            jobtemplate=path_mynemo+'/NEMO/job_multi_'+machine+'.ksh'
            use_template(jobtemplate, jobname, {'NODE':node,'CORE':core,'TIME':time,'TMPDIR':str(tmpdir_exp),'CONFEXP':path_mynemo+'/NEMO/CONFIGS/'+config+'/'+name,'KK':jobnb})
            subprocess.call(["chmod", "+x", jobname])
        mpmdname=tmpdir_exp+'/mpmd.conf'
        if not os.path.exists(mpmdname):
            mpmdtemplate=path_mynemo+'/NEMO/template_mpmd.conf'
            core_xiosm1=int(core_xios)-1
            cores_m1=int(core)-1
            if int(core_xios)+int(core_nemo) != int(core):
                sys.exit('Wrong repartition of cores between nemo and xios')
            else:
                use_template(mpmdtemplate, mpmdname, {'XIOS':str(core_xiosm1),'NEMO1':core_xios,'NEMO2':cores_m1})
                subprocess.call(["chmod", "+x", mpmdname])
    else:
        jobtemplate=path_mynemo+'/NEMO/job_'+machine+'.ksh'
        use_template(jobtemplate, jobname, {'NODE':node,'CORE':core,'TIME':time,'TMPDIR':str(tmpdir_exp),'CONFEXP':path_mynemo+'/NEMO/CONFIGS/'+name,'KK':jobnb})
        subprocess.call(["chmod", "+x", jobname])

    #We also set up the output and restart job before launching
    joboname=tmpdir_exp+'/job_output'+str(jobnb)+'.ksh'
    if not os.path.exists(joboname):
        jobotemplate=path_mynemo+'/NEMO/job_output_'+machine+'.ksh'
        use_template(jobotemplate, joboname, {'TMPDIR':tmpdir_exp,'CONFCASE':name,'SDIR':sdir_exp_work,'KK':jobnb})
        subprocess.call(["chmod", "+x", joboname])
    
    jobrname=tmpdir_exp+'/job_restart'+str(jobnb)+'.ksh'
    if not os.path.exists(jobrname):
        jobrtemplate=path_mynemo+'/NEMO/job_restart_'+machine+'.ksh'
        use_template(jobrtemplate, jobrname, {'TMPDIR':tmpdir_exp,'CONFCASE':name,'NITEND':nitend,'RDIR':rdir_exp_work})
        subprocess.call(["chmod", "+x", jobrname])

    #Launch the main job
    runname=tmpdir_exp+'/run'+str(jobnb)+'.ksh'
    if not os.path.exists(runname):
        runtemplate=path_mynemo+'/NEMO/run.ksh'
        use_template(runtemplate, runname, {'SUB':jobsub,'TMPDIR':str(tmpdir_exp),'KK':jobnb})
        subprocess.call(["chmod", "+x", runname])

    continue_question('We are about to launch the job in '+tmpdir_exp+' check that everything is ok,')
    subprocess.run(runname,shell=True)

    print('You can check the progress of your job with qmt command and the progression of NEMO with tail -f ocean.output and tts')

def gather_init(all_files,tmpdir_exp,path_input):
    """
    Make links to the init files in the tmp_dir for the exp
    """
    for filefrc in all_files:
        if os.path.exists(path_input+'/'+filefrc):
            if not os.path.exists(tmpdir_exp+'/'+filefrc):
                os.symlink(path_input+'/'+filefrc, tmpdir_exp+'/'+filefrc)
        else:
            sys.exit(filefrc+' is not available in '+path_input+' go fix that and relaunch start')

def gather_forc(all_files,tmpdir_exp,path_forc,years):
    """
    Make links to the forcing files in the tmp_dir for the exp
    """
    for filefrc in all_files:
        for year in years:
            filefrc_year=filefrc+'_y'+year+'.nc'
            if not os.path.exists(tmpdir_exp+'/'+filefrc_year):
                if os.path.exists(path_forc+'/'+filefrc_year):
                    os.symlink(path_forc+'/'+filefrc_year, tmpdir_exp+'/'+filefrc_year)
                else:
                    sys.exit(filefrc_year+' is missing from '+path_forc+' fix this and relaunch the start')

def years_forc(nit0,nitend,dt,date_init):
    """
    Make a list of all the years of forcing that are needed to run this segment defined by first and last time step, duration of the time-step and the starting datea of the segment
    """
    year1=str(date_init)[0:4]
    years=[year1]
    length=(int(nitend)-int(nit0)+1)*int(dt)
    if length/(3600*24) > 334:
        #We need 3 years of forcing
        years.append(str(int(year1)-1))
        years.append(str(int(year1)+1))
    else:
        #It depends on the start date
        month1=str(date_init)[4:6]
        if int(month1) == 1:
            #We need current and previous year
            years.append(str(int(year1)-1))
        elif int(month1) == 12:
            #We need current and next year
            years.append(str(int(year1)+1))
    return years

def compile_tool(machine,arch,nemo_version,tool_name,path_nemo,path_mynemo):
    """
    Compile the tool_name distributed with NEMO on machine
    """
    print('Now we are going to compile the selected tool')
    #Looking for the proper arch file + adding the xios version in it
    archname='arch-'+str(arch)+'.fcm'
    if not os.path.exists(path_nemo+'/arch/CNRS/'+archname):
        if not os.path.exists(path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname):
            templatename=path_mynemo+'/NEMO/'+nemo_version+'/arch/template_arch-'+str(compiler)+'_xios_path.fcm'
            use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname, {'PATH_XIOS':str(path_xios)})
        print('We copy the '+str(archname)+' arch file to '+path_nemo+'/arch/CNRS')
        shutil.copyfile(path_mynemo+'/NEMO/'+nemo_version+'/arch/'+archname,path_nemo+'/arch/CNRS/'+archname)

    #A script to compile the reference config with proper arch file
    scriptname='compile_'+str(tool_name)+'_'+arch+'.ksh'
    if not os.path.exists(path_nemo+'/tools/'+scriptname):
        if not os.path.exists(path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname):
            templatename=path_mynemo+'/NEMO/template_compile_tool.ksh'
            use_template(templatename, path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname, {'ARCH':str(arch),'PATH':path_nemo+'/tools/','TOOL':str(tool_name)})
    shutil.copyfile(path_mynemo+'/NEMO/'+nemo_version+'/'+scriptname,path_nemo+'/tools/'+scriptname)
    subprocess.call(["chmod", "+x", path_nemo+'/tools/'+scriptname])
    print('Go to '+path_nemo+'/tools and compile the tool '+str(tool_name)+' with '+str(scriptname))
    continue_question('If successfully compiled,')
    continue_question('Now that is has been successfully compiled, add '+tool_name+' to the list all_tools and all_exec_tool to lists.py,')

