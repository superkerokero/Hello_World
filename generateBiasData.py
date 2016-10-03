# coding: utf-8

""" generateBiasData.py:
    This is a script used to generate &biasdata for H-REMD
    in FreeFlex."""

import polygonGen
import json
import sys
import os
import argparse


def writeExample(input_file_name):
    "This is a function to write example input file."
    fi = dict()
    fi["initial_polygon"] = ((0.0, 0.0), (0.0, 2.0), (4.0, 4.0), (4.0, 0.0))
    fi["intervals"] = (1.0, 1.0)
    fi["sub_polygons"] = (((0.0, 0.0), (0.0, 2.0), (4.0, 4.0), (4.0, 0.0)),
                          ((2.0, 0.0), (2.0, 4.0), (4.0, 4.0), (4.0, 0.0)))
    fi["x_biassec"] = ("TESTX 1 1 1 3.1", "0.e0")
    fi["y_biassec"] = ("TESTY 1 1 2 1.0 2.0", "0.e0")
    fi["sample_dir"] = os.getcwd() + "/files/samples"
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
            sys.exit("writeFiles: Error during open file \'" +
                     cfilename + "\'. Check if the file exists.")


def writeFiles(filename, strout):
    "Write &biasdata and replicaID files."
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
        
        
def generateData(info):
    "Generate data based on given info."
    # First create the total poly.
    poly = polygonGen.Polygon(info["initial_polygon"],
                              info["intervals"])
    # Create sub-polys from total poly.
    sub_poly_info = list()
    for tpoly in info["sub_polygons"]:
        sub_poly_info.append(poly.generateSubSet(tpoly, 20))
    # Convert core-based data into coord-based data.
    coord_based = list()
    for sub_poly in sub_poly_info:
        coord_based.append(poly.core2coord(sub_poly[0]))
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
    return [str_data, str_id]
    

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
                    samples[value] = os.path.join(root, f)
                except ValueError:
                    print "Unrecognizable file ignored: " + f
    print "Successfully recognized %d samples." % len(samples)
    return samples


# Perform following operations if the script is run directly.
if __name__ == "__main__":
    arguments = cmdParse()
    if arguments.example_gen:
        writeExample(arguments.input_file_name)
        sys.exit("Generated example file name: " +
                 arguments.input_file_name)
    if arguments.sample_gen:
        createSample("sample_")
        sys.exit("Generation of samples completed.")
    info = readFile(arguments.input_file_name)
    sout = generateData(info)
    writeFiles((arguments.output_file_name,
                arguments.output_repidfile_name), sout)
    if arguments.sample_use:
        samples = getSamples("files/samples/")

