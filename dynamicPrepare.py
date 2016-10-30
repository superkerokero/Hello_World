# coding: utf-8

""" dynamicPrepare.py:
    This is a script used to generate initial structs for H-REMD
    in FreeFlex from the previous round and given parameters."""

import json
import os
import sys
import argparse
import shutil

def processData(param_json, repid_file, last_file, struct_file, num):
    "Read data from input json files and repid files."
    # Open a param_json file to read in point parameters.
    previous = repid_file + str(num-1)
    current = repid_file + str(num)
    rSet = readJson(param_json)
    preID = readRepid(previous)
    curID = readRepid(current)
    # Find closest index for current.
    index = dict()
    for k1, v1 in curID.iteritems():
        temp = sys.float_info.max
        for k2, v2 in preID.iteritems():
            d = (rSet[v1][0]-rSet[v2][0]) ** 2 + \
                (rSet[v1][1]-rSet[v2][1]) ** 2
            if d < temp:
                temp = d
                index[k1] = k2
    # Copy files based on index.
    print index
    cwd = os.getcwd()
    for key, value in index.iteritems():
        src = cwd + "/" + str(value-1).zfill(4) + "/" + \
                   last_file + str(num-1)
        dst = cwd + "/" + str(key-1).zfill(4) + "/" + \
                 struct_file + str(num)
        try:
            shutil.copyfile(src, dst)
        except shutil.Error:
            sys.exit("Target and source are the same!")
        except IOError:
            sys.exit("The destination is not writtable!")
        
def readJson(filename):
    "Open a given file to read in parameters."
    try:
        with open(filename, "rU") as funit:
            string = funit.read()
    except IOError:
        sys.exit("readFile: Error during open file \'" + filename +
                 "\'. Check if the file exists.")
    return json.loads(string)

def readRepid(filename):
    "Read data from repid file and store in a dict."
    repid = dict()
    try:
        with open(filename, "rU") as funit:
            for string in funit:
                raw = string.split()
                repid[int(raw[0])] = raw[1]
    except IOError:
        sys.exit("readFile: Error during open file \'" + filename +
                 "\'. Check if the file exists.")
    return repid

def cmdParse():
    "Parse the command line argument for parameters."
    parser = argparse.ArgumentParser(description="Dynamically prepare struct_files.")
    parser.add_argument("-j", nargs="?", dest="pj",
                        default="param.json", metavar="filename",
                        help="input param json file name.")
    parser.add_argument("-r", nargs="?", dest="rep",
                        default="repid", metavar="filename",
                        help="input repid file name(without numbering) to be used.")
    parser.add_argument("-s", nargs="?", dest="st",
                        default="struct_", metavar="filename",
                        help="Struct file name to be output.")
    parser.add_argument("-l", nargs="?", dest="last",
                        default="lastms", metavar="filename",
                        help="Reference struct file(original).")
    parser.add_argument("-n", nargs="?", type=int, dest="num",
                        default=2, metavar="N",
                        help="Number of the round to be started.")
    return parser.parse_args()


# Perform following actions if the script is run directly.
if __name__ == "__main__":
    args = cmdParse()
    processData(args.pj, args.rep, args.last, args.st, args.num)
    print "Succesfully processed structs for the next round! {0}".format(args.num)
