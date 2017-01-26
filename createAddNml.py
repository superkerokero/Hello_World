# coding: utf-8

""" createAddNml.py:
    This is a script used to generate initial ms files using packmol
    for FreeFlex."""

import json
import os
import sys
import argparse
import subprocess as sp
import shutil

def addBlock(nml_file, data):
    "Add block info to nml_file."
    try:
        with open(nml_file, "a") as f:
            f.write("\n&add\n") # first line.
            f.write("  file = " + data["file"] + "\n") # file line.
            f.write("  n = " + data["n"] + "\n") # n line.
            f.write("  velocity = " + data["velocity"] + "\n") # velocity line.
            f.write("  direction = " + data["direction"] + "\n") # direction line.
            f.write("  exclude = " + data["exclude"] + "\n") # exclude line.
            f.write("  exclude2 = " + data["exclude2"] + "\n") # exclude2 line.
            f.write("  exclude3 = " + data["exclude3"] + "\n") # exclude3 line.
            f.write("\/\n")
    except IOError:
        sys.exit("addBlock: Error during appending file \'" + nml_file + "\'.")

def systemBlock(nml_file, system):
    "Initialize file using system data."
    try:
        if os.path.exists(nml_file):
            print "{0} already exists, overwriting...".format(nml_file)
            os.remove(nml_file)
        with open(nml_file, "w+") as f:
            f.write("\n&system\n") # first line.
            f.write("  size = " + system["size"] + "\n") # size line.
            f.write("  Tinit = " + system["Tinit"] + "\n") # Tinit line.
            f.write("\/\n")
    except IOError:
        sys.exit("systemBlock: Error during writing file \'" + nml_file + "\'.")

def addBlockPackmol(nml_file, data):
    "Add block info to nml_file."
    try:
        with open(nml_file, "a") as f:
            f.write("structure " + data["structure"] + "\n") # first line.
            f.write("  number " + data["number"] + "\n") # file line.
            f.write(data["details"] + "\n") # details line.
            f.write("end structure\n") # last line.
            f.write("\n")
    except IOError:
        sys.exit("addBlock: Error during appending file \'" + nml_file + "\'.")

def systemBlockPackmol(nml_file, system):
    "Initialize file using system data."
    try:
        if os.path.exists(nml_file):
            print "{0} already exists, overwriting...".format(nml_file)
            os.remove(nml_file)
        with open(nml_file, "w+") as f:
            f.write("tolerance " + system["tolerance"] + "\n") # first line.
            f.write("output " + system["output"] + "\n") # output line.
            f.write("filetype " + system["filetype"] + "\n") # filetype line.
            f.write("\n") # blank line.
    except IOError:
        sys.exit("systemBlock: Error during writing file \'" + nml_file + "\'.")

def createDataPackmol(zeta, wcoord, nw, workdir):
    "Create data for writing blocks in packmol."
    # from meter to angstrom.
    zeta *= 1.e10
    wcoord *= 1.e10
    # create empty container.
    data = [dict(), dict(), dict(), dict(), dict()]
    pos_ion = zeta - 42.5
    pos_wf = pos_ion - wcoord
    n_wf_water = int(round((pos_wf - 1. + 30.)*2./3.))
    if n_wf_water < 0: n_wf_water = 0
    # ion
    data[0]["structure"] = workdir + "cl.xyz"
    data[0]["number"] = "1"
    data[0]["details"] = "  center\n" + "  fixed 0. 0. " + \
                         str(pos_ion) + " 0. 0. 0."
                         # -42.5 is the position of water COM.  
    # ion cluster water
    data[1]["structure"] = workdir + "water.xyz"
    data[1]["number"] = str(nw)
    data[1]["details"] = "  inside cube -2.5 -2.5 " + \
                         str(pos_ion - 2.5) + " 5."
                         # -42.5 - 5./2. = 45.

    # water finger water (invalid when zeta < 12.5 + 3.0 = 15.5)
    data[2]["structure"] = workdir + "water.xyz"
    data[2]["number"] = str(n_wf_water)
    data[2]["details"] = "  inside box -1.5 -1.5 -30. " + \
                         " 1.5 1.5 " + str(pos_wf - 1.)
                         # 1. angstrom for cluster (if any).
    # bulk water water
    data[3]["structure"] = workdir + "water.xyz"
    data[3]["number"] = str(523 - nw - n_wf_water)
    data[3]["details"] = "  inside cube -12.5 -12.5 -55. 25."

    # bulk dcm
    data[4]["structure"] = workdir + "dcm.xyz"
    data[4]["number"] = "500"
    if n_wf_water > 0:
        data[4]["details"] = "  inside box -12.5 -12.5 -30. 12.5 12.5 55.\n" + \
                             "  outside cube -2.5 -2.5 " + str(pos_ion -2.5) + \
                             " 5.\n" + \
                             "  outside box -1.5 -1.5 -30. 1.5 1.5 " + str(pos_wf - 1.)
    else:
        data[4]["details"] = "  inside box -12.5 -12.5 -30. 12.5 12.5 55.\n" + \
                             "  outside cube -2.5 -2.5 " + str(pos_ion -2.5) + \
                             " 5."
    return [data, n_wf_water]
        
def readJson(filename):
    "Open a given file to read in parameters."
    try:
        with open(filename, "rU") as funit:
            string = funit.read()
    except IOError:
        sys.exit("readFile: Error during open file \'" + filename +
                 "\'. Check if the file exists.")
    return json.loads(string)

    
def readParam(param_json):
    "Read param_json file that contains all replica coordinates."
    rSet = readJson(param_json)
    return rSet

def readRepid(filename):
    "Read data from repid file and store in a dict."
    repid = dict()
    try:
        with open(filename, "rU") as funit:
            for string in funit:
                raw = string.split()
                repid[raw[0]] = raw[1]
    except IOError:
        sys.exit("readFile: Error during open file \'" + filename +
                 "\'. Check if the file exists.")
    return repid

def cmdParse():
    "Parse the command line argument for parameters."
    parser = argparse.ArgumentParser(
        description= "Automate W.F. initial structure creation using packmol.")
    parser.add_argument("-i", nargs="?", dest="inp",
                        default="inp.json", metavar="filename",
                        help="input param json file name.")
    return parser.parse_args()


# Perform following actions if the script is run directly.
if __name__ == "__main__":
    args = cmdParse()
    inp = readParam(args.inp)
    os.chdir(inp["workdir"])
    rSet = readParam(inp["paramList"]) # rSet data.
    system = dict()
    system["tolerance"] = inp["tolerance"]
    system["filetype"] = inp["filetype"]
    # loop lv1.
    for ii in range(inp["rounds"]):
        repid = readRepid(inp["repid"] + str(ii + 1)) # current repid_file.
        n_dir = len(repid) # total number of dirs.
        # loop lv2.
        for i in range(n_dir):
            # create directories.
            newdir = inp["workdir"] + "/" + str(i).zfill(4) + "/"
            try:
                os.mkdir(newdir)
            except OSError:
                pass
            # create input file for packmol.
            system["output"] = inp["workdir"] + str(i).zfill(4) + "/" + \
                               inp["xyz_output"] + str(ii + 1) + ".xyz"
            systemBlockPackmol(inp["packmol_file"], system)
            data = createDataPackmol(rSet[repid[str(i + 1)]][0],
                                     rSet[repid[str(i + 1)]][1], inp["nw"], inp["workdir"])
            for iii in range(len(data[0])):
                if data[1] == 0 and iii == 2: continue
                addBlockPackmol(inp["packmol_file"], data[0][iii])
            # call packmol to create xyz file.
            command = inp["packmol_exe"] + " < " + inp["packmol_file"]
            ret =  sp.call(command, shell=True)
            if ret == 0:
                print "Successfully created packmol input file: {0} {1}!".format(ii + 1, i + 1)
            else:
                sys.exit("Packmol {0} {1} finished with return code {2}".format(ii + 1, i + 1, ret))
            # call xyz2ms to cerate ms file.
            command = inp["xyz2ms_exe"] + " " + inp["workdir"] + str(i).zfill(4) + "/" + \
                               inp["xyz_output"] + str(ii + 1) + ".xyz " + inp["ms_input"] + \
                               " " + inp["workdir"] + str(i).zfill(4) + "/" + \
                               inp["ms_output"] + str(ii + 1)
            
            ret =  sp.call(command, shell=True)
            if ret == 0:
                print "Successfully converted xyz file: {0} {1}!".format(ii, i)
            else:
                sys.exit("xyz2ms.exe {0} {1} finished with return code {2}".format(ii, i, ret))
            
        print "Succesfully processed structs for round {0} !".format(ii + 1)
