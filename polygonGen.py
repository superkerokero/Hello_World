# coding: utf-8

""" polygonGen.py:
    This is a module used to generate quadrilateral sample points based on
    input: N points(N>=3) defining a polygon area inside the sampling space."""


class Polygon(object):
    def __init__(self, init_points, intervals):
        "Constructor of the class."
        self.points = init_points
        self.intervals = intervals
        self.rSet = self.generateSet(self.points, intervals)
        
    @staticmethod
    def _linearEquation(vector):
        """Convert vector to a line of infinite length.
        We want the line in linear equation standard form: a*x + b*y + c = 0
        See: http://en.wikipedia.org/wiki/Linear_equation"""
        a = vector[1][1] - vector[0][1]
        b = vector[0][0] - vector[1][0]
        c = (vector[1][0]*vector[0][1]) - (vector[0][0]*vector[1][1])
        return (a, b, c)
        
    def _areIntersecting(self, vector1, vector2):
        """Calculates whether two vectors are intersecting each other.
           0: not intersecting
           1: intersecting(once)
           2: collinear(arbitrary intersecting points)"""
        # calculate the line of vector1.
        line1 = self._linearEquation(vector1)
        # insert points of vector2 into line1 and check if vector2 intersects.
        d1 = line1[0]*vector2[0][0] + line1[1]*vector2[0][1] + line1[2]
        d2 = line1[0]*vector2[1][0] + line1[1]*vector2[1][1] + line1[2]
        # if d1 and d2 share the same sign, two vectors don't intersect.
        if d1*d2 > 0:
            return 0
        """The fact that vector 2 intersected the infinite line 1 above doesn't
           mean it also intersects the vector1. Vector1 is only a subset of
           that infinite line1, so it may have intersected that line before
           the vector started or after it ended. To know for sure, we have to
           repeat the same test the other way round. We start by calculating
           the infinite line2 in linear equation standard form."""
        line2 = self._linearEquation(vector2)
        d1 = line2[0]*vector1[0][0] + line2[1]*vector1[0][1] + line2[2]
        d2 = line2[0]*vector1[1][0] + line2[1]*vector1[1][1] + line2[2]
        if d1*d2 > 0:
            return 0
        """If we get here, only two possibilities are left. Either the two
           vectors intersect in exactly one point or they are collinear, which
           means they intersect in any number of points."""
        if line1[0]*line2[1] - line2[0]*line1[1] == 0.0e0:
            return 2
        # If they are not collinear, they must be intersecting once.
        return 1
        
    def rayCastingInside(self, polygon, point):
        """Calculates how often intersects the ray(defined by the given point
           and an arbitrary point outside the polygon) a polygon side. Then
           decide whether the point is within the polygon."""
        # avoid "vertex on the tip" problem.
        if list(point) in polygon:
            return True
        # set the point that is outside of the polygon.
        bound = (min(polygon, key=(lambda x: x[0]))[0] - 1.0, point[1])
        # initialize intersections counter.
        edge = (polygon[0], polygon[len(polygon) - 1])
        # solve the "ray on the vertex" problem.
        ymax = max(edge[0][1], edge[1][1])
        ymin = min(edge[0][1], edge[1][1])
        if point[1] == ymax or point[1] == ymin:
            tpoint = (point[0], point[1] + 1.e-10*abs(ymax))
        else:
            tpoint = point
        intersects = self._areIntersecting((bound, tpoint), edge)
        # loop all edges of the polygon and count total intersections.
        for i in range(1, len(polygon)):
            edge = (polygon[i-1], polygon[i])
            # solve the "ray on the vertex" problem.
            ymax = max(edge[0][1], edge[1][1])
            ymin = min(edge[0][1], edge[1][1])
            if point[1] == ymax or point[1] == ymin:
                tpoint = (point[0], point[1] + 1.e-10*abs(ymax))
            else:
                tpoint = point
            intersects += self._areIntersecting((bound, tpoint), edge)
        # check inside/outside by odd/even intersection counts.
        if intersects % 2 == 0:
            # loop through all edges to see if the point is on any of them.
            edge = (polygon[0], polygon[len(polygon) - 1])
            if self._pointOnEdge(edge, tpoint):
                return True
            for i in range(1, len(polygon)):
                edge = (polygon[i-1], polygon[i])
                if self._pointOnEdge(edge, tpoint):
                    return True
            return False
        else:
            return True
            
    def generateSet(self, points, intervals):
        "Generate point sets using given intervals for given polygon."
        xmax = max(points, key=(lambda x: x[0]))[0]
        xmin = min(points, key=(lambda x: x[0]))[0]
        ymax = max(points, key=(lambda x: x[1]))[1]
        ymin = min(points, key=(lambda x: x[1]))[1]
        # initialization.
        rSet = dict()
        nSet = 0
        # try to add first point.
        x = xmin
        y = ymin
        # add rest points.
        while x <= xmax:
            while y <= ymax:
                if self.rayCastingInside(self.points, (x, y)):
                    nSet += 1
                    rSet[nSet] = (x, y)
                y += intervals[1]
            x += intervals[0]
            y = ymin
        return rSet
        
    def _pointOnEdge(self, edge, point):
        "See if the point is on the edge."
        xmax = max(edge[0][0], edge[1][0])
        xmin = min(edge[0][0], edge[1][0])
        ymax = max(edge[0][1], edge[1][1])
        ymin = min(edge[0][1], edge[1][1])
        if xmin <= point[0] <= xmax and ymin <= point[1] <= ymax:
            line = self._linearEquation(edge)
            dis = line[0]*point[0] + line[1]*point[1] + line[2]
            if dis == 0.0:
                return True
        return False

    @staticmethod
    def core2coord(rSet):
        "Translate core-based set into coordinate-based set."
        dict_x = {}
        dict_y = {}
        # first create empty dicts with correct keys.
        for key in rSet:
            dict_x[rSet[key][0]] = set()
            dict_y[rSet[key][1]] = set()
        # then fill the dicts with correct values.
        for key in rSet:
            dict_x[rSet[key][0]].add(key)
            dict_y[rSet[key][1]].add(key)
        return [dict_x, dict_y]
        
    def generateSubSet(self, polygon, max_nSet):
        "Generate subSet from self.rSet that lies within given polygon."
        nSet = 0
        # this is for storing subSet dict.
        subSet = dict()
        # we need a table to tell what the ID in the subSet is in the rSet.
        subSetID = dict()
        for key in self.rSet:
            if self.rayCastingInside(polygon, self.rSet[key]):
                nSet += 1
                subSetID[nSet] = key
                subSet[nSet] = self.rSet[key]
                if nSet == max_nSet:
                    print "Reached max_nSet."
                    print "Given set number: %d" % max_nSet
                    print "Last point in the set: {0}".format(subSet[nSet])
                    return (subSet, subSetID)
        # extend the polygon when there are remaining cores to be used.
        temp = [polygon, max_nSet, nSet, subSet, subSetID]
        for i in range(5):
            if temp[2] != max_nSet:
                temp = self.extendSubSet(i, *temp)
            else:
                break
        if temp[2] != max_nSet:
            print "Given polygon was filled before reaching given set "+ \
                "number after 5 extends."
            print "Given set number: %d" % max_nSet
            print "Generated set number: %d" % temp[2]
            print "Last point in the set: {0}".format(temp[3][temp[2]])
        return (temp[3], temp[4])

    def extendSubSet(self, num, polygon, max_nSet, nSet, subSet, subSetID):
        "Extend subpoly from bottom left to contain more cores."
        print "Given polygon was filled before reaching given set "+ \
            "number."
        print "Given set number: %d" % max_nSet
        print "Generated set number: %d" % nSet
        print "#{0} Extending from bottomleft to fill in remaining cores...".format(num)
        minX = min(polygon, key = lambda x: x[0])[0]
        maxX = max(polygon, key = lambda x: x[0])[0]
        minY = min(polygon, key = lambda x: x[1])[1]
        newY = minY - self.intervals[1]
        new_polygon = [(minX, newY), (minX, minY), (maxX, minY), (maxX, newY)]
        for key in self.rSet:
            if self.rayCastingInside(new_polygon, self.rSet[key]):
                nSet += 1
                print "nSet: {0}".format(nSet)
                subSetID[nSet] = key
                subSet[nSet] = self.rSet[key]
                if nSet == max_nSet:
                    print "Reached max_nSet(Ex.{0}).".format(num)
                    print "Given set number: %d" % max_nSet
                    print "Last point in the set: {0}".format(subSet[nSet])
                    break
        return [new_polygon, max_nSet, nSet, subSet, subSetID]
