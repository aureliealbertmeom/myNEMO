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

#Get the parameters for this new experiment and the specific job we are going to launch
dic_tool=f.read_single_yaml("current_tool.yml")

machine=dic_tool['machine']
arch=dic_tool['arch']
nemo_version=dic_tool['nemo']
tool_name=dic_tool['name']
if 'config' in dic_tool:
    config=dic_tool['config']

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

path_nemo=ls.all_path_nemo[machine][nemo_version]

#If tool is already compiled
path_tool=path_nemo+'/tools/'+tool_name
if tool_name in ls.all_tools[machine][nemo_version]:
    print(str(tool_name)+" has been compiled on "+str(machine)+" and is located at "+str(path_tool))
#Lets compile the tool
else:
    f.compile_tool(machine,arch,nemo_version,tool_name,path_nemo,path_mynemo)

#Use of the tool for a CONFIG
if 'config' in dic_tool:
    print(str(tool_name)+" will be used for config "+config)
    path_use_tool=path_work+'/'+config+'/'+config+'-I/'+tool_name
    if not os.path.exists(path_use_tool):
            os.makedirs(path_use_tool)

    for exec_tool in ls.all_exec_tool[tool_name]:
        if not os.path.exists(path_use_tool+'/'+exec_tool):
            if os.path.exists(path_tool+'/'+exec_tool):
                os.symlink(path_tool+'/'+exec_tool, path_use_tool+'/'+exec_tool)
            else:
                sys.exit(tool_name+' has not been properly compiled, the executable '+exec_tool+' could not be found')

    for nam_tool in ls.all_nam_tool[tool_name]:
        if not os.path.exists(path_use_tool+'/'+nam_tool):
            if os.path.exists(path_mynemo+'/NEMO/tools/'+tool_name+'/'+nam_tool):
                shutil.copyfile(path_mynemo+'/NEMO/tools/'+tool_name+'/'+nam_tool,path_use_tool+'/'+nam_tool)

    print("All is ready at "+path_tool)

