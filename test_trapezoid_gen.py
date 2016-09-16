# coding: utf-8
#!/usr/bin/env python
"""The test module for trapezoid_gen module."""

import unittest
import trapezoid_gen

class TestModule(unittest.TestCase):
    """Unittest extend."""
    def setUp(self):
        "setup initial conditions for test."
        init_points = [[0.0, 0.0], [0.0, 2.0], [4.0, 4.0], [4.0, 0.0]]
        intervals = [1.0, 1.0]
        max_core = 50
        overlap = 0.5
        self.test = trapezoid_gen.Trapezoid(init_points, intervals, \
                                            max_core, overlap)
    def tearDown(self):
        "destructor for test."
        del self.test
    def test_checkborder(self):
        "test the _checkborder function."
        self.assertTrue(self.test._checkborder([0.0, 2.0]))
        self.assertFalse(self.test._checkborder([5.0, 4.0]))
    def test_generate_sets(self):
        "test generate_sets function."
        #plus 1 is needed for accounting the endpoints.
        expected_size = int((self.test.points[2][0] - self.test.points[0][0])/ \
                self.test.intervals[0]) + 1
        self.assertEqual(expected_size, len(self.test.generate_sets()[0]))

#Perform unittest if the script is run directly.
if __name__ == "__main__":
    unittest.main()
