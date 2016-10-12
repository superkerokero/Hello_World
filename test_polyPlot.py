
# coding: utf-8
"""The test module for polygonGen module."""

import unittest
import polyPlot
import numpy as np

class TestModule(unittest.TestCase):
    """Unittest extend."""
    def setUp(self):
        "setup initial conditions for test."
        size = 20
        sets = dict()  
        xarray = np.linspace(0.0, 10.0, size)
        yarray = np.linspace(2.0, 20.0, size)
        for i in range(size):
            sets[i] = (xarray[i], yarray[i])
        self.test = polyPlot.polyPlot()
        self.test.addPolygon(sets, vz = 1.0)

    def tearDown(self):
        "destructor for test."
        del self.test
        
    def test_showPlot(self):
        "test the showPlot function."
        self.test.showPlot()
        # self.assertEqual()
                         

# Perform unittest if the script is run directly.
if __name__ == "__main__":
    unittest.main()
