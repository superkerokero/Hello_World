# coding: utf-8

""" 
mreusBot.py:
This is a bot that uses subprocess module for
automating a series of mreus simulations using
FreeFlex.
"""

import subprocess as sp
import json
import sys
import os
import argparse
import time



def writeExample(input_file_name):
    "This is a function to write example input file."
    fi = dict()
    fi["exec_path"] = "/home/wanglj/FreeFlex/FreeFlex.exe"
    fi["work_path"] = "/home/wanglj/multi_reus/multi1"
    fi["n_core"] = 112
    fi["machinefile"] = "mpd.hosts"
    fi["head_nml"] = "mreusnml_"
    # Using "pretty printing" format.
    sinput = json.dumps(fi, sort_keys=True, indent=4)
    try:
        os.mkdir("files")
        print "Created directory \'files\'."
    except OSError:
        print "Directory \'files\' already exists."
    try:
        if os.path.exists(input_file_name):
            os.remove(input_file_name)
        with open(input_file_name, "w+") as wfile:
            wfile.write(sinput)
    except IOError:
        print "writeExample: Error during open wfile." + \
              "Check if the file already exists." + input_file_name


def readFile(filename):
    "Open a given file to read in parameters."
    try:
        with open(filename, "rU") as funit:
            string = funit.read()
    except IOError:
        sys.exit("readFile: Error during open file \'" + filename +
                 "\'. Check if the file exists.")
    return json.loads(string)


def cmdParse():
    "Parse the command line argument for parameters."
    parser = argparse.ArgumentParser(description="Generate biasdata.")
    parser.add_argument("-ex", action="store_true", dest="example_gen",
                        help="Generate example input file if this arg" +
                        " exists.")
    parser.add_argument("-i", nargs="?", dest="input_file_name",
                        default="files/botconfig.json", metavar="filename",
                        help="input file name.")
    parser.add_argument("-s", nargs="?", dest="n_start",
                        default=1, metavar="number",
                        help="Number of starting set.")
    parser.add_argument("-e", nargs="?", dest="n_end",
                        default=4, metavar="number",
                        help="Number of the last set..")
    return parser.parse_args()


def argsGen(info, i):
    "Generate arguments used by bot."
    args = list()
    args.append("mpiexec")
    args.append("-machinefile")
    args.append(info["machinefile"])
    args.append("-n")
    args.append(str(info["n_core"]))
    args.append(info["exec_path"])
    args.append(info["head_nml"] + str(i))
    return args


def startBot(info, args):
    "Start bot using subprocess.call."
    os.chdir(info["work_path"])
    for i in range(args.n_start, args.n_end+1):
        print "Round {0} started.".format(i)
        args = argsGen(info, i)
        ret =  sp.call(args, shell=False)
        if ret == 1:
            print "Sim{0} finished successfully!".format(i)
            print "Sleep for 100s to avoid mpiexec deadlock."
            time.sleep(100)
            print "Wake up, starting round {0}!".format(i+1)
        else:
            sys.exit("Sim{0} finished with return code {1}".format(i, ret))


# Perform following operations if the script is run directly.
if __name__ == "__main__":
    arguments = cmdParse()
    if arguments.example_gen:
        writeExample(arguments.input_file_name)
        sys.exit("Generated example file name: " +
                 arguments.input_file_name)
    info = readFile(arguments.input_file_name)
    startBot(info, arguments)
