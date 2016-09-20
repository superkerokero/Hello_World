# coding: utf-8

""" trapezoid_gen.py:
    This is a module used to generate trapozoid points based on
    input: four points defining a trapozoid area inside the sampling space.
           (type: tuple of tuples)"""


class Trapezoid(object):
    "Class for the trapezoid generation."
    def __init__(self, init_points, intervals, max_core, overlap):
        """Constructor of the class(Trapezoid_gen).
           The numberings of points (x,y) in the trapezoid are given as below.
           y
           |
           2----------------------------3
           |                            |
           |                            |
           1----------------------------4 ===== x"""

        self.points = init_points
        self.intervals = intervals
        self.max_core = max_core
        self.total_point = 0
        self.overlap = overlap
        try:
            self.slope = (self.points[2][1]-self.points[1][1]) \
                         /(self.points[2][0]-self.points[1][0])
        except ZeroDivisionError:
            print "The slope has a zero division error, " + \
                  "please check the input points"
    def _checkborder(self, point):
        "Check whether a point is inside the border."
        bottom = (point[1] >= self.points[0][1])
        left = (point[0] >= self.points[0][0])
        right = (point[0] <= self.points[3][0])
        border = ((point[1]-self.points[1][1]) <= self.slope* \
                  (point[0]-self.points[1][0]))
        return bottom and left and right and border
    def _init_dict(self, start, end, interval):
        """Initialize dict with all keys ranging from start to end
           having initial value of 0."""
        idict = {}
        temp = start
        while temp <= end:
            idict[temp] = set()
            temp += interval
        return idict
    def generate_sets(self):
        "The function that generates trapezoid sets."
        print "Start generating trapezoid points based on input data."
        #generate empty dict for 1st & 2nd coordinates.
        dict_x = self._init_dict(self.points[0][0], self.points[3][0], \
                self.intervals[0])
        dict_y = self._init_dict(self.points[0][1], self.points[2][1], \
                self.intervals[1])
        #add the bottom-left point to dicts.
        num_core = 1
        #list = in python is call-by-reference.
        #in order to copy into a new list that is irrelevant to the
        #original one, you can use either:
            #current_point = list(self.points[0])
            #or as below.
        current_point = self.points[0][:]
        dict_x[current_point[0]].add(num_core)
        dict_y[current_point[1]].add(num_core)
        while True:
            num_core += 1
            current_point[1] += self.intervals[1]
            if self._checkborder(current_point):
                #if the updated point is within border, add directly.
                dict_x[current_point[0]].add(num_core)
                dict_y[current_point[1]].add(num_core)
            else:
                #if the updated point exceeds border, update x value
                #and reset y value.
                current_point[0] += self.intervals[0]
                current_point[1] = self.points[0][1]
                if self._checkborder(current_point):
                    dict_x[current_point[0]].add(num_core)
                    dict_y[current_point[1]].add(num_core)
                else:
                    num_core -= 1 #Exclude the last out-of-border point.
                    print "Generated %d points" % num_core
                    self.total_point = num_core
                    break
        print "Raw list generation completed."
        return [dict_x, dict_y]
    def translate_sets(self, input_set):
        "Translate coordinate-based set into core-based set."
        dict_core = {}
        for key in input_set[0]:
            for core in input_set[0][key]:
                dict_core[core] = [key]
        for key in input_set[1]:
            for core in input_set[1][key]:
                dict_core[core].append(key)
        return dict_core
