# coding: utf-8

""" generateBiasData.py:
    This is a script used to generate &biasdata for H-REMD
    in FreeFlex."""

import polygonGen
import json
import sys
import os
import argparse
import shutil


def writeExample(input_file_name):
    "This is a function to write example input file."
    fi = dict()
    fi["initial_polygon"] = ((0.0, 0.0), (0.0, 2.0), (2.0, 2.0), (2.0, 0.0))
    fi["intervals"] = (1.0, 1.0)
    fi["sub_polygons"] = (((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)),
                          ((2.0, 0.0), (2.0, 4.0), (4.0, 4.0), (4.0, 0.0)))
    fi["x_biassec"] = ("TESTX 1 1 1 3.1", "0.e0")
    fi["y_biassec"] = ("TESTY 1 1 2 1.0 2.0", "0.e0")
    fi["tx_biassec"] = ("TESTtotalX 1 1 1 3.1", "0.e0")
    fi["ty_biassec"] = ("TESTtotalY 1 1 2 1.0 2.0", "0.e0")
    fi["sample_dir"] = os.getcwd() + "/files/samples"
    fi["headstr"] = "newsample"
    fi["struct_dir"] = os.getcwd() + "/files/structs"
    fi["max_ncore"] = 100
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


def createSample(filename):
    "Create sample files for testing."
    try:
        os.makedirs("files/samples")
        print "Created directory \'files/samples\'."
    except OSError:
        print "Directory \'files/samples\' already exists."
    numbers = list()
    for i in range(20):
        numbers.append(float(i))
    for number in numbers:
        cfilename = "files/samples/" + filename + str(number)
        try:
            if os.path.exists(cfilename):
                os.remove(cfilename)
            with open(cfilename, "w+") as funit:
                funit.write(str(number)+"\n")
        except IOError:
            sys.exit("createSample: Error during open file \'" +
                     cfilename + "\'. Check if the file exists.")
    print "Successfully generated " + str(len(numbers)) + \
          " sample files for test."


def readFile(filename):
    "Open a given file to read in parameters."
    try:
        with open(filename, "rU") as funit:
            string = funit.read()
    except IOError:
        sys.exit("readFile: Error during open file \'" + filename +
                 "\'. Check if the file exists.")
    return json.loads(string)
    

def writeFile(filename, strout):
    "Write given string(s) into file(s)."
    count = 0
    for string in strout:
        count += 1
        cfilename = filename + str(count)
        try:
            if os.path.exists(cfilename):
                os.remove(cfilename)
            with open(cfilename, "w+") as funit:
                funit.write(string)
        except IOError:
            sys.exit("writeFile: Error during open file \'" +
                     cfilename + "\'. Check if the file exists.")


def writeFiles(filename, strout):
    "Write &biasdata and replicaID files."
    # write total &biasdata file.
    cfilename = filename[0] + "_total"
    try:
        if os.path.exists(cfilename):
            os.remove(cfilename)
        with open(cfilename, "w+") as funit:
            funit.write(strout[3])
    except IOError:
        sys.exit("writeFiles: Error during open file \'" +
                 cfilename + "\'.")

    # write the &biasdata file.
    writeFile(filename[0], strout[0])
    # write the replicaID file.
    writeFile(filename[1], strout[1])
    print "Successfully written output " + str(len(strout[0])*2) + \
          " file(s)."


def set2str(inset):
    "Convert set data into string(no parentheses)."
    string = ""
    for element in inset:
        string += (str(element) + " ")
    return string


def dict2str(indict):
    "Convert single dict (key: value) pair into string(no parentheses)."
    string = ""
    for key, value in indict.iteritems():
        string += str(key) + " " + str(value) + "\n"
    return string


def countPointPairs(iSet, intervals):
    """Given a set of points, count the number of adjacent pairs
       (including diagonal pairs)."""
    count = 0
    # setting eps to account for round-off errors in float.
    eps = 1.0e-18
    for p, v in iSet.iteritems():
        for tp, tv in iSet.iteritems():
            A = abs(v[0]-tv[0]) <= eps
            B = abs(v[1]-tv[1]) <= eps
            C = abs(abs(v[0]-tv[0])-intervals[0]) <= eps
            D = abs(abs(v[1]-tv[1])-intervals[1]) <= eps
            logicA = A and D
            logicB = B and C
            logicC = C and D
            if logicA or logicB or logicC:
                count+=1
    # every pair was counted twice.
    return count/2

        
def generateData(info):
    "Generate data based on given info."
    # First create the total poly.
    poly = polygonGen.Polygon(info["initial_polygon"],
                              info["intervals"])
    # Create the coord-based data containing all sets in the main poly.
    coord_total = poly.core2coord(poly.rSet)
    strout = "&biasdata\n"
    for key, value in coord_total[0].iteritems():
        strout += (info["tx_biassec"][0] + " " + str(key) + " " +
                   info["tx_biassec"][1] + " " + set2str(value) + "\n")
    for key, value in coord_total[1].iteritems():
        strout += (info["ty_biassec"][0] + " " + str(key) + " " +
                   info["ty_biassec"][1] + " " + set2str(value) + "\n")
    str_total = strout + "&end\n"
    # Create sub-polys from total poly.
    sub_poly_info = list()
    for tpoly in info["sub_polygons"]:
        sub_poly_info.append(poly.generateSubSet(tpoly, info["max_ncore"]))
    # Convert core-based data into coord-based data.
    coord_based = list()
    count = 0
    for sub_poly in sub_poly_info:
        count += 1
        coord_based.append(poly.core2coord(sub_poly[0]))
        npairs = countPointPairs(sub_poly[0], info["intervals"])
        print "Subpoly {0} has {1} potential pairs.".format(count, npairs)
    # Convert dict data into writable strings.
    str_data = list()
    # The coord_based contains multiple [dict_x, dict_y] pairs.
    for data in coord_based:
        strout = "&biasdata\n"
        for key, value in data[0].iteritems():
            strout += (info["x_biassec"][0] + " " + str(key) + " " +
                       info["x_biassec"][1] + " " + set2str(value) + "\n")
        for key, value in data[1].iteritems():
            strout += (info["y_biassec"][0] + " " + str(key) + " " +
                       info["y_biassec"][1] + " " + set2str(value) + "\n")
        strout += "&end\n"
        str_data.append(strout)
    # Convert id list into string.
    str_id = list()
    for each_info in sub_poly_info:
        strout = dict2str(each_info[1])
        str_id.append(strout)
    return [str_data, str_id, coord_based, str_total]


def cmdParse():
    "Parse the command line argument for parameters."
    parser = argparse.ArgumentParser(description="Generate biasdata.")
    parser.add_argument("-ex", action="store_true", dest="example_gen",
                        help="Generate example input file if this arg" +
                        " exists.")
    parser.add_argument("-i", nargs="?", dest="input_file_name",
                        default="files/example_input", metavar="filename",
                        help="input file name.")
    parser.add_argument("-o", nargs="?", dest="output_file_name",
                        default="files/example_output", metavar="filename",
                        help="output file name for biasdata.")
    parser.add_argument("-repid", nargs="?", dest="output_repidfile_name",
                        default="files/repid", metavar="filename",
                        help="output file name for replica id list.")
    parser.add_argument("-sample", action="store_true", dest="sample_gen",
                        help="Generate a series of samples for " +
                        "tesing if this arg exists.")
    parser.add_argument("-uses", action="store_true", dest="sample_use",
                        help="Use generated samples to create MD initial " +
                        "conditions.")
    return parser.parse_args()


def getSamples(workdir, headstr="sample_"):
    """Recieve a path name and get sample files that starts with headstr
       contained in it."""
    samples = dict()
    for root, dirs, files in os.walk(workdir):
        for f in files:
            if f.startswith(headstr):
                try:
                    value = float(f[len(headstr):])
                    samples[str(value)] = os.path.join(root, f)
                except ValueError:
                    print "Unrecognizable file ignored: " + f
    print "Successfully recognized %d samples." % len(samples)
    return samples


def copySamples(coord_based, samples, workdir, coord_id=0):
    "Copy samples into designated workdir according to coord values."
    # create root dir for copied files.
    try:
        os.mkdir(workdir)
    except OSError:
        print "The \'%s\' already exists." % workdir
    count = 0
    for data in coord_based:
        count += 1
        for key, value in data[coord_id].iteritems():
            if str(key) in samples:
                for core in value:
                    newdir = workdir + "/" + str(core-1).zfill(4) + "/"
                    try:
                        os.mkdir(newdir)
                    except OSError:
                        pass
                    try:
                        shutil.copyfile(samples[str(key)], newdir + "struct_" + \
                                        str(count))
                    except shutil.Error:
                        sys.exit("Target and source are the same!")
                    except IOError:
                        sys.exit("The destination is not writtable!")
            else:
                sys.exit("The file with value \'" + str(key) + \
                         "\' wasn't found. Check the sample folder.")
    print "Successfully copied sample files."


# Perform following operations if the script is run directly.
if __name__ == "__main__":
    arguments = cmdParse()
    if arguments.example_gen:
        writeExample(arguments.input_file_name)
        sys.exit("Generated example file name: " +
                 arguments.input_file_name)
    info = readFile(arguments.input_file_name)
    if arguments.sample_gen:
        createSample(info["headstr"])
        sys.exit("Generation of samples completed.")
    sout = generateData(info)
    writeFiles((arguments.output_file_name,
                arguments.output_repidfile_name), sout)
    if arguments.sample_use:
        samples = getSamples(info["sample_dir"], info["headstr"])
        copySamples(sout[2], samples, info["struct_dir"])
