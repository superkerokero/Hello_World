# coding: utf-8

"""
polyPlot.py:
This module uses matplotlib to plot all generated polygons
using generateBiasData.py.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class polyPlot(object):
    """
    The class that provides basic plotting functions. 
    """
    def __init__(self):
        "The constructor of the class polyPlot."
        fig = plt.figure(1)
        self.ax = fig.gca(projection='3d')

    def addPolygon(self, sets, vz = 0.e0, color="b"):
        "Add points to draw at a certain z value."
        size = len(sets)
        x = np.zeros(size)
        y = np.zeros(size)
        for key, value in sets.iteritems():
            x[key-1] = value[0]
            y[key-1] = value[1]
        self.ax.scatter(x, y, vz, c=color)

    def showPlot(self):
        "Show all added points."
        plt.show()
