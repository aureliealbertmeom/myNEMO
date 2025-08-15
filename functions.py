#! /usr/bin/env python
import sys
import shutil
import subprocess
import inquirer
import yaml


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
        case "Continue":
            print("We will proceed with the next step")

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
