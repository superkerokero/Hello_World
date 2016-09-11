#!/usr/bin/env python

""" trapozoid_gen.py:
    This is a module used to generate trapozoid points based on
    input: four points defining a trapozoid area inside the sampling space.
           (type: tuple of tuples)"""

import unittest

class Trapezoid(object):
    "Class for the trapezoid generation."
    def __init__(self, init_points):
        """Constructor of the class(Trapezoid_gen).
           The numberings of points (x,y) in the trapezoid are given as below.
           y
           |
           2----------------------------3
           |                            |
           |                            |
           1----------------------------4 ===== x"""

        self.points = init_points
        try:
            self.slope = (self.points[2][1]-self.points[1][1]) \
                         /(self.points[2][0]-self.points[1][0])
        except ZeroDivisionError:
            print "The slope has a zero division error, \
                   please check the input points"
    def _checkborder(self, point):
        """Check whether a point is inside the border."""
        bottom = (point[1] >= self.points[0][1])
        left = (point[0] >= self.points[0][0])
        right = (point[0] <= self.points[3][0])
        border = ((point[1]-self.points[1][1]) >= self.slope* \
                  (point[0]-self.points[1][0]))
        return bottom and left and right and border
    def _normalize(self)
    
