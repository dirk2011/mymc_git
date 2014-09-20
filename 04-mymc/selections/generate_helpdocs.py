#!/usr/bin/python
"""
Ergens gevonden op internet, handig python script, om documentatie
te dumpen in tekst bestanden.
help documenteert de bestanden is in de interpreter aanwezig als
help en in zit in de pydoc module.

ref:
http://stackoverflow.com/questions/11265603/how-do-i-export-the-output-of-pythons-built-in-help-function
"""

import sys
import pydoc
import os

def output_help_to_file(filepath, request):
    f = file(filepath, 'w')
    sys.stdout = f
    pydoc.help(request)
    f.close()
    sys.stdout = sys.__stdout__
    return

# output_help_to_file(r'os.txt', 'os')
sys.path.append('/media/rasp163-v/mymc/04-mymc')

output_help_to_file(r'selections.txt', 'selections')
output_help_to_file(r'selections_temp.txt', 'selections_temp')
