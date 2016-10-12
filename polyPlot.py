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

    def addPolygon(self, sets, vz = 0.e0):
        "Add points to draw at a certain z value."
        size = len(sets)
        x = np.zeros(size)
        y = np.zeros(size)
        z = np.ones(size) * vz
        for key, value in sets.iteritems():
            x[key] = value[0]
            y[key] = value[1]
        self.ax.plot(x, y, z)

    def showPlot(self):
        "Show all added points."
        plt.show()
