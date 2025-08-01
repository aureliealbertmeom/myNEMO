#! /usr/bin/env python
import sys
import shutil
import subprocess

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
