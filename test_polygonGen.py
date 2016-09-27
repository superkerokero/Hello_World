
# coding: utf-8
"""The test module for polygonGen module."""

import unittest
import polygonGen


class TestModule(unittest.TestCase):
    """Unittest extend."""
    def setUp(self):
        "setup initial conditions for test."
        init_points = ((0.0, 0.0), (0.0, 2.0), (4.0, 4.0), (4.0, 0.0))
        self.test = polygonGen.Polygon(init_points)

    def tearDown(self):
        "destructor for test."
        del self.test
        
    def test_linearEquation(self):
        "test the _linearEquation function."
        self.assertEqual(self.test._linearEquation(((0.0, 2.0), (0.0, 0.0))),
                         (-2.0, 0.0, 0.0))
        self.assertEqual(self.test._linearEquation(((1.0, 1.0), (2.0, 2.0))),
                         (1.0, -1.0, 0.0))
                         
    def test_areIntersecting(self):
        "test the _areIntersecting function."
        # test for no intersecting.
        self.assertEqual(self.test._areIntersecting(((1.0, 1.0), (2.0, 2.0)),
                         ((2.0, 1.0), (4.0, 1.0))), 0)
        # test for intersecting.
        self.assertEqual(self.test._areIntersecting(((1.0, 1.0), (2.0, 2.0)),
                         ((0.0, 1.0), (4.0, 1.0))), 1)
        # test for collinear.
        self.assertEqual(self.test._areIntersecting(((1.0, 1.0), (2.0, 2.0)),
                         ((1.5, 1.5), (4.5, 4.5))), 2)
        # test for collinear(but not intersecting).
        self.assertEqual(self.test._areIntersecting(((1.0, 1.0), (2.0, 2.0)),
                         ((3.5, 3.5), (4.5, 4.5))), 2)
                                                    
    def test_rayCastingInside(self):
        "test the rayCastingInside function."
        self.assertTrue(self.test.rayCastingInside(self.test.points,
                        (4.0, 2.0)))
        self.assertFalse(self.test.rayCastingInside(self.test.points,
                         (3.0, 4.0)))
                        
    def test_generateSet(self):
        "test the generateSet function."
        self.assertEqual(len(self.test.generateSet(self.test.points,
                         (2.0, 2.0))), 7)
                         
    def test_pointOnEdge(self):
        "test the _pointOnEdge function."
        self.assertTrue(self.test._pointOnEdge(((1.0, 1.0), (4.0, 4.0)),
                                               (1.2, 1.2)))

# Perform unittest if the script is run directly.
if __name__ == "__main__":
    unittest.main()
