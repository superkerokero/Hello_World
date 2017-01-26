# coding: utf-8

""" changeParam.py:
    This is a script used to change specified parameters in ms file. 
"""

import json
import os
import sys
# import argparse
import subprocess as sp
# import shutil

def readJson(filename):
    "Open a given file to read in parameters."
    try:
        with open(filename, "rU") as funit:
            string = funit.read()
    except IOError:
        sys.exit("readFile: Error during open file \'" + filename +
                 "\'. Check if the file exists.")
    return json.loads(string)

def runSubProcess(exe_path, ms_input, ms_output, site_name,
                  param_name, param_value):
    "run subprocess using given parameters."
    command = exe_path + " " + ms_input + " " + ms_output + " " + \
              site_name + " " + param_name + " " + param_value
    ret =  sp.call(command, shell=True)
    if ret == 0:
        print "Successfully changed param: {0}\n{1}\n{2}\n{3}\n".format(
            ms_output, site_name, param_name, param_value)
    else:
        sys.exit("param_change.exe finished with return code {0}".format(ret))
    
def cmdParse():
    "Parse the command line argument for parameters."
    parser = argparse.ArgumentParser(
        description= "Automate ms file parameter change using param_change.exe")
    parser.add_argument("-i", nargs="?", dest="inp",
                        default="paramChange.json", metavar="filename",
                        help="input param json file name.")
    return parser.parse_args()


# Perform following actions if the script is run directly.
if __name__ == "__main__":
    args = cmdParse()
    inp = readJson(args.inp)
    os.chdir(inp["workdir"])
    for key, value in inp["sites"].iteritems():
        for ii in range(inp["rounds"]):
            for i in range(inp["ndir"]):
                ms_input = inp["workdir"] + str(i).zfill(4) + "/" + inp["ms_input"] + str(ii)
                ms_output = inp["workdir"] + str(i).zfill(4) + "/" + inp["ms_output"] + str(ii)
                runSubProcess(inp["exe_path"], ms_input, ms_output,
                              key, *value)
