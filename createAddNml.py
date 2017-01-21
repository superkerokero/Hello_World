# coding: utf-8

""" initialAdd.py:
    This is a script used to generate &nml for add.exe
    in FreeFlex."""

import json
import os
import sys
import argparse
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
    parser.add_argument("-i", nargs="?", dest="pj",
                        default="inp.json", metavar="filename",
                        help="input param json file name.")
    return parser.parse_args()


# Perform following actions if the script is run directly.
if __name__ == "__main__":
    args = cmdParse()
    rSet = readParam(args.pj) # rSet data.
    n_dir = len(repid) # total number of dirs.
    # loop lv1.
    for ii in range(args.num):
        repid = readRepid(args.rep + str(ii + 1)) # current repid_file.
        # loop lv2.
        for i in range(n_dir):
            # create directories.
            newdir = args.wd + "/" + str(i).zfill(4) + "/"
            try:
                os.mkdir(newdir)
            except OSError:
                pass
        print "Succesfully processed structs for the next round! {0}".format(args.num)
