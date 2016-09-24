# coding: utf-8
"""The test module for polygonGen module."""

import unittest
import polygonGen

class TestModule(unittest.TestCase):
    """Unittest extend."""
    def setUp(self):
        "setup initial conditions for test."
        init_points = [[0.0, 0.0], [0.0, 2.0], [4.0, 4.0], [4.0, 0.0]]
        intervals = [1.0, 1.0]
        max_core = 5
        overlap = 0.5
        self.test = polygonGen.Polygon(init_points)
    def tearDown(self):
        "destructor for test."
        del self.test
    def test_checkborder(self):
        "test the _checkborder function."
        self.assertTrue(self.test._checkborder([0.0, 2.0]))
        self.assertFalse(self.test._checkborder([5.0, 4.0]))
        print "hoo!"


#Perform unittest if the script is run directly.
if __name__ == "__main__":
    unittest.main()
