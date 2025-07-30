import os
import re
import sys
from pprint import pprint
import shutil
import subprocess

sys.path.append(os.path.realpath("."))
import inquirer  
import lists as ls


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
xios_version=answer4[q4]

if xios_version in ls.all_tag_xios[machine]:
        path_xios=ls.all_path_xios[machine][xios_version]
        print("Version "+str(xios_version)+" has been compiled on "+str(machine)+" and is located at "+str(path_xios))

else:
        print("We are going to compile XIOS on "+str(machine))
        q5="xios-version2"
        question5 = [ inquirer.List(q5,message="What big category of XIOS version do you want to compile?",choices=["1","2","3"]) ]
        answer5 = inquirer.prompt(question5)
        xios_version2=answer5[q5]
        q6a="xios-tag-bool"
        question6a = [ inquirer.List(q6a,message="Do you have a specific tag in mind?",choices=["yes","no"]) ]
        answer6a = inquirer.prompt(question6a)
        xios_tag_bool=answer6a[q6a]
        match xios_tag_bool:
            case "yes":
                q6="xios-tag"
                question6 = [ inquirer.Text(q6,message="Which specific tag do you have in mind?") ]
                answer6 = inquirer.prompt(question6)
                xios_tag=answer6[q6]
                xios_version_tag='XIOS'+str(xios-version2)+'_'+str(xios_tag)
                if xios_version_tag in ls.all_tag_xios[machine]:
                    path_xios=ls.all_path_xios[machine][xios_version_tag]
                    print("Version "+str(xios_version_tag)+" has been downloaded on "+str(machine)+" and is located at "+str(path_xios))
                else:
                    scriptname=ls.all_path_dev[machine]+'myNEMO/XIOS/get_xios'+str(xios_version2)+'-'+str(xios_tag)+'.sh'
                    if not os.path.exists(scriptname):
                        templatename=ls.all_path_dev[machine]+'myNEMO/XIOS/get_xios_tag.sh'
                        shutil.copyfile(templatename,scriptname)
                        subprocess.call(["sed", "-i", "-e",  's%VERS%'+str(xios_version2)+'%g',scriptname])
                        subprocess.call(["sed", "-i", "-e",  's%TAG%'+str(xios_tag)+'%g',scriptname])
                    print('Then use the get_xios'+str(xios_version2)+'-'+str(xios_tag)+'.sh script located in the subrepo XIOS to download XIOS')
            case "no":
                scriptname=ls.all_path_dev[machine]+'myNEMO/XIOS/get_xios'+str(xios_version2)+'.sh'
                if not os.path.exists(scriptname):
                    templatename=ls.all_path_dev[machine]+'myNEMO/XIOS/get_xios_notag.sh'
                    shutil.copyfile(templatename,scriptname)
                    subprocess.call(["sed", "-i", "-e",  's%VERS%'+str(xios_version2)+'%g',scriptname])
                print('Then use the get_xios'+str(xios_version2)+'.sh script located in the subrepo XIOS to download trunk version of XIOS'+str(xios_version2))
        
        q7="continue"
        question7= [ inquirer.List(q7,message="Proceed with the download and if it is successful hit continue", choices=["Continue","Stop"]) ]
        answer7 = inquirer.prompt(question7)
        continue_bool1=answer7[q7]

        match continue_bool1:
            case "Stop":
                sys.exit("Exiting, bye")
            case "Continue":
                #check if the corresponding compile_xios script already exists
                scriptname=ls.all_path_dev[machine]+'myNEMO/XIOS/compile_xios_'+str(ls.all_arch_xios[machine])+'.sh'
                if not os.path.exists(scriptname):
                    templatename=ls.all_path_dev[machine]+'myNEMO/XIOS/compile_xios_arch.sh'
                    shutil.copyfile(templatename,scriptname)
                    subprocess.call(["sed", "-i", "-e",  's%ARCH%'+str(ls.all_arch_xios[machine])+'%g',scriptname])
                    print("Now you just have to compile XIOS using the compile_xios_"+str(ls.all_arch_xios[machine])+".sh script that is available in XIOS subdirectory") 
                q7a="continue"
                question7a = [ inquirer.List(q7a,message="Proceed with the compilation and if it is successful hit continue", choices=["Continue","Stop"]) ]
                answer7a = inquirer.prompt(question7a)
                continue_bool1=answer7a[q7a]
                match continue_bool1:
                    case "Stop":
                        sys.exit("Exiting, bye")
                    case "Continue":
                        print('You can now modify list.py to add XIOS version '+str(xios_version)+' for machine '+str(machine)

#NEMO version
q8="nemo-version"
choices_nemo_version=ls.all_tag_nemo[machine].copy()
choices_nemo_version.append("else")
question8 = [ inquirer.List(q8,message="What version of NEMO would you like to use?",choices=choices_nemo_version) ]
answer8 = inquirer.prompt(question8)
nemo_version=answer8[q8]

if nemo_version in ls.all_tag_nemo[machine]:
        path_nemo=ls.all_path_nemo[machine][nemo_version]
        print("Version "+str(nemo_version)+" has been downloaded on "+str(machine)+" and is located at "+str(path_nemo))

else:
        print("We are going to download NEMO on "+str(machine))
        scriptname=ls.all_path_dev[machine]+'myNEMO/NEMO/get_nemo'+str(nemo_version)+'.sh'
        if not os.path.exists(scriptname):
            templatename=ls.all_path_dev[machine]+'myNEMO/NEMO/get_nemo_tag.sh'
            shutil.copyfile(templatename,scriptname)
            subprocess.call(["sed", "-i", "-e",  's%TAG%'+str(nemo_version)+'%g',scriptname])
        print('Then use the get_nemo'+str((nemo_version))+'.sh script located in the subrepo NEMO to download NEMO')





                




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
