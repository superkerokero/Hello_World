# coding: utf-8

""" generateBiasData.py:
    This is a script used to generate &biasdata for H-REMD 
    in FreeFlex."""

import polygonGen
import json
import sys


def writeExample():
    "This is a function to write example input file."
    fi = dict()
    fi["initial_polygon"] = ((0.0, 0.0), (0.0, 2.0), (4.0, 4.0), (4.0, 0.0))
    fi["intervals"] = (1.0, 1.0)
    fi["sub_polygons"] = (((0.0, 0.0), (0.0, 2.0), (4.0, 4.0), (4.0, 0.0)),
                          ((2.0, 0.0), (2.0, 4.0), (4.0, 4.0), (4.0, 0.0)))
    fi["x_biassec"] = ("x ", " and ")
    fi["y_biassec"] = ("y ", " and ")
    # Using "pretty printing" format.
    sinput = json.dumps(fi, sort_keys=True, indent=4)
    try:
        with open("example_input", "r+U") as wfile:
            wfile.write(sinput)
    except IOError:
        print "Error during open wfile. Check if the file already exists."

def readFile(f):
    "Open a given file to read in parameters."
    try:
        with open(f, "rU") as funit:
            string = funit.read()
    except IOError:
        sys.exit("Error during open file \'"+f+"\'. Check if the file exists.")
    return json.loads(string)

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
        strout = ""
        for key, value in data[0].iteritems():
            strout += (info["x_biassec"][0] + str(key) + info["x_biassec"][1] +
                       set2str(value) + "\n")
        for key, value in data[1].iteritems():
            strout += (info["y_biassec"][0] + str(key) + info["y_biassec"][1] +
                       set2str(value) + "\n")
        str_data.append(strout)
    # Convert id list into string.
    str_id = list()
    for each_info in sub_poly_info:
        strout = dict2str(each_info[1])
        str_id.append(strout)
    return [str_data, str_id]


# Perform following operations if the script is run directly.
if __name__ == "__main__":
    writeExample()
    info = readFile("example_input")
    sout = generateData(info)

