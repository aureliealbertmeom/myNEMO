import os
import re
import sys
from pprint import pprint
import subprocess

sys.path.append(os.path.realpath("."))
#library for interactions
import inquirer  
#module gathering all the parameters, path etc
import lists as ls
#some functions
import functions as f

#Trivial question to start, allows to exit in case of running by mistake
q1="start"
question1 = [ inquirer.List(q1,message="So you want to run a NEMO experiment?",choices=["yes","no"]) ]
answer1 = inquirer.prompt(question1)

match answer1[q1]:
    case "no":
        sys.exit("Goodbye then")

#Supercomputers used, the list will grow as it will be used
q2="machine"
question2 = [ inquirer.List(q2,message="On which machine?",choices=["irene","else"]) ]
answer2 = inquirer.prompt(question2)
machine=answer2[q2]
match machine:
    case "irene":
        print(str(machine)+" it is !")
        path_dev=ls.all_path_store[machine]
        path_work=ls.all_path_store[machine]
        path_scratch=ls.all_path_store[machine]
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

#New or recycling an existing experiment
q3="existing-exp"
question3 = [ inquirer.List(q3,message="Do you want to replicate an existing experiment?",choices=["yes","no"]) ]
answer3 = inquirer.prompt(question3)
match answer3[q3]:
    case "yes":
        sys.exit("Sorry, no experiments have been designed yet")

#XIOS version
q4="xios-version"
choices_xios_version=ls.all_tag_xios[machine].copy()
choices_xios_version.append("else")
question4 = [ inquirer.List(q4,message="What version of XIOS would you like to use?",choices=choices_xios_version) ]
answer4 = inquirer.prompt(question4)
xios_version_tag=answer4[q4]

#If XIOS version is already installed and compiled
if xios_version_tag in ls.all_tag_xios[machine]:
    path_xios=ls.all_path_xios[machine][xios_version_tag]
    print("Version "+str(xios_version_tag)+" has been compiled on "+str(machine)+" and is located at "+str(path_xios))

#A new version of XIOS for this machine has to be downloaded and compiled
else:
    print("We are going to compile XIOS on "+str(machine))
    q5="xios-version2"
    question5 = [ inquirer.List(q5,message="What big category of XIOS version do you want to compile?",choices=["1","2","3"]) ]
    answer5 = inquirer.prompt(question5)
    xios_version=answer5[q5]
    q6a="xios-tag-bool"
    question6a = [ inquirer.List(q6a,message="Do you have a specific tag in mind?",choices=["yes","no"]) ]
    answer6a = inquirer.prompt(question6a)
    xios_tag_bool=answer6a[q6a]
    match xios_tag_bool:
        #A specific tag is identified
        case "yes":
            q6="xios-tag"
            question6 = [ inquirer.Text(q6,message="Which specific tag do you have in mind?") ]
            answer6 = inquirer.prompt(question6)
            xios_tag=answer6[q6]
            scriptname=ls.all_path_dev[machine]+'/myNEMO/XIOS/get_xios'+str(xios_version)+'-'+str(xios_tag)+'.ksh'
            if not os.path.exists(scriptname):
                templatename=ls.all_path_dev[machine]+'/myNEMO/XIOS/template_get_xios_tag.ksh'
                f.use_template(templatename, scriptname, {'VERS':str(xios_version),'TAG':str(xios_tag)})
            print('Then use the get_xios'+str(xios_version)+'-'+str(xios_tag)+'.sh script located in the subrepo XIOS to download XIOS')
            xios_version_tag=str(xios_version)+'-'+str(xios_tag)
        #No specific tag, we take the current trunk version
        case "no":
            scriptname=ls.all_path_dev[machine]+'myNEMO/XIOS/get_xios'+str(xios_version)+'.sh'
            if not os.path.exists(scriptname):
                templatename=ls.all_path_dev[machine]+'myNEMO/XIOS/template_get_xios_notag.sh'
                f.use_template(templatename, scriptname, {'VERS':str(xios_version)})
            print('Then use the get_xios'+str(xios_version)+'.sh script located in the subrepo XIOS to download trunk version of XIOS'+str(xios_version))
            q6="xios-tag"
    q7="continue"
    question7= [ inquirer.List(q7,message="Proceed with the download and if it is successful hit continue", choices=["Continue","Stop"]) ]
    answer7 = inquirer.prompt(question7)
    continue_bool1=answer7[q7]

    match continue_bool1:
        case "Stop":
            sys.exit("Exiting, bye")
        case "Continue":
            #We want to know which tag we end up with
            if xios_tag_bool == "no":
                q7a="tag"   
                question7a = [ inquirer.Text(q7a,message="Which tag did you end up with? (svn info will tell you)") ]
                answer7a = inquirer.prompt(question7a)
                xios_tag=answer7a[q7a]
                xios_version_tag=str(xios_version)+'-'+str(xios_tag)
            #The path depends on the version AND tag    
            path_xios=ls.all_path_dev[machine]+'/xios'+str(xios_version)+'-trunk-'+str(xios_tag)
        
            #A script with the proper arch to compile on this machine
            scriptname=ls.all_path_dev[machine]+'myNEMO/XIOS/compile_xios_'+str(arch_xios)+'.sh'
            #check if the corresponding compile_xios script already existsif not os.path.exists(scriptname):
                templatename=ls.all_path_dev[machine]+'myNEMO/XIOS/template_compile_xios_arch.sh'
                f.use_template(templatename, scriptname, {'ARCH':str(arch_xios)})
            print("Now you just have to compile XIOS using the compile_xios_"+str(arch_xios)+".sh script that is available in XIOS subdirectory") 
            #Compilation is complete
            q7b="continue"
            question7b = [ inquirer.List(q7b,message="Proceed with the compilation and if it is successful hit continue", choices=["Continue","Stop"]) ]
            answer7b = inquirer.prompt(question7b)
            continue_bool2=answer7b[q7b]
            match continue_bool2:
                case "Stop":
                    sys.exit("Exiting, bye")
                case "Continue":
                    print('You can now modify list.py to add XIOS version '+str(xios_version)+' for machine '+str(machine)+' in all_tag_xios and the associated path in all_path_xios')

#NEMO version
q8="nemo-version"
choices_nemo_version=ls.all_tag_nemo[machine].copy()
choices_nemo_version.append("else")
question8 = [ inquirer.List(q8,message="What version of NEMO would you like to use?",choices=choices_nemo_version) ]
answer8 = inquirer.prompt(question8)
nemo_version=answer8[q8]

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
    q8a="continue"
    question8a = [ inquirer.List(q8a,message="Proceed with the download and if it is successful add it to the list in list.py in all_tag_nemo and hit continue", choices=["Continue","Stop"]) ]
    answer8a = inquirer.prompt(question8a)
    continue_bool3=answer8a[q8a]
    match continue_bool3:
        case "Stop":
            sys.exit("Exiting, bye")

#Compilation of a ref case
print('Now we are going to compile the selected version of NEMO with the previously selected version of XIOS')
#Looking for the proper arch file + adding the xios version in it
archname=ls.all_path_dev[machine]+'/myNEMO/NEMO/arch/arch-'+str(arch_nemo)+'_'+str(xios_version_tag)+'.fcm'
if not os.path.exists(archname):
    templatename=ls.all_path_dev[machine]+'myNEMO/NEMO/arch/template_arch-'+str(arch_nemo)+'_xios_path.fcm'
    f.use_template(templatename, scriptname, {'PATH_XIOS':str(path_xios)})
print('Copy the '+str(archname)+' arch file to '+str(path_dev)+'/'+str(nemo_version)+'/arch/CNRS')

#Choose a reference config to start with
q9="ref_config"
choices_nemo_ref_configs=ls.all_ref_conf_nemo[nemo_version]
question9 = [ inquirer.List(q9,message="What reference configuration of NEMO would you like to use?",choices=choices_nemo_ref_configs) ]
answer9 = inquirer.prompt(question9)
nemo_ref_conf=answer9[q9]

#A script to compile the reference config with proper arch file
scriptname=ls.all_path_dev[machine]+'/myNEMO/NEMO/compile_nemo_'+str(nemo_ref_conf)+'_'+str(arch_nemo)+'_'+str(xios_version_tag)+'.ksh'
templatename=ls.all_path_dev[machine]+'/myNEMO/NEMO/template_compile_config_ref_arch.ksh'
f.use_template(templatename, scriptname, {'ARCH':str(arch_nemo)+'_'+str(xios_version_tag),'REFCONF':str(nemo_ref_conf)})
print('Copy and use the script '+str(scriptname)+'  NEMO to '+str(path_dev)+'/'+str(nemo_version)+' to compile the '+str(nemo_ref_conf)+' reference with selected version of XIOS ')





                




#New question
#qxx=""
#questionxx = [ inquirer.List(qxx,message="?",choices=["yes","no"]) ]
#answerxx = inquirer.prompt(questionxx)
#new_question=answerxx[qxx]
#
#match new_question:
#    case "yes":
#        pprint("")
#
#    case "no":
#        sys.exit("")
