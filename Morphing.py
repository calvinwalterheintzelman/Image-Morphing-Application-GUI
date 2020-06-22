#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       4/13/2019
#######################################################

import os
import sys
import numpy as np
from scipy.spatial import Delaunay
import imageio

#######################################################

class Triangle:

    def error(self):
        raise ValueError('Input must be 3 x 2 numpy array of type "float64"')

    def __init__(self, vertices):
        if not(isinstance(vertices, np.ndarray)):
            self.error()
        if len(vertices) != 3:
            self.error()
        for two_list in vertices:
            if not(isinstance(two_list, np.ndarray)):
                self.error()
            if len(two_list) != 2:
                self.error()
        for two_list in vertices:
            for element in two_list:
                if not(isinstance(element, np.float64)):
                    self.error()
        self.vertices = vertices

    def _det(self, point1, point2):
        return point1[0]*point2[1] - point1[1]*point2[0]


    def getPoints(self):
        max_x = int(np.trunc(max(self.vertices[0][0], self.vertices[1][0], self.vertices[2][0])))
        max_y = int(np.trunc(max(self.vertices[0][1], self.vertices[1][1], self.vertices[2][1])))
        min_x = int(np.trunc(min(self.vertices[0][0], self.vertices[1][0], self.vertices[2][0])))
        min_y = int(np.trunc(min(self.vertices[0][1], self.vertices[1][1], self.vertices[2][1])))
        v0 = self.vertices[0]
        s1 = [self.vertices[1][0] - v0[0], self.vertices[1][1] - v0[1]]
        s2 = [self.vertices[2][0] - v0[0], self.vertices[2][1] - v0[1]]

        inside_points = []
        for x in range(min_x, max_x + 1):
            keep_going = True
            for y in range(min_y, max_y + 1):
                point = [np.float64(x), np.float64(y)]

                #using formula point_in_triangle = v0 + a*s1 + b*s2
                a = np.true_divide(self._det(point, s2) - self._det(v0, s2), self._det(s1, s2))
                b = np.true_divide(self._det(v0, s1) - self._det(point, s1), self._det(s1, s2))

                if a >= np.float64(0) and b >= np.float64(0) and a + b <= np.float64(1):
                    inside_points.append(point)
                    keep_going = False
                elif not(keep_going):
                    break
        return inside_points

def loadTriangles(leftPointFilePath, rightPointFilePath):
    l_file = open(leftPointFilePath, 'r')
    r_file = open(rightPointFilePath, 'r')
    l_line = l_file.readline()
    r_line = r_file.readline()
    if l_line == "" or r_line == "":
        return ([], [])

    l_points = []
    while l_line != '':
        l_points.append([np.float64(l_line[0:8]), np.float64(l_line[8:16])])
        l_line = l_file.readline()
        
    l_points = np.array(l_points)
    if len(l_points) < 3:
        return ([], [])
    l_tris = Delaunay(l_points)
    leftTriangles = []
    for triangle in l_points[l_tris.simplices]:
        leftTriangles.append(Triangle(triangle))

    r_points = []
    while r_line != '':
        r_points.append([np.float64(r_line[0:8]), np.float64(r_line[8:16])])
        r_line = r_file.readline()

    r_points = np.array(r_points)
    rightTriangles = []
    for triangle in r_points[l_tris.simplices]:
        rightTriangles.append(Triangle(triangle))

    l_file.close()
    r_file.close()

    return (leftTriangles, rightTriangles)

class Morpher:

    def _initError(self):
        raise TypeError("Triangles must be list of type Triangle, Images must be numpy arrays of type numpy.uint8")

    def __init__(self, leftImage, leftTriangles, rightImage, rightTriangles):
        if not(isinstance(leftImage, np.ndarray)) or not(isinstance(rightImage, np.ndarray)):
            self._initError()
        for row in leftImage:
            if not(isinstance(row, np.ndarray)):
                self._initError()
            for col in row:
                if not(isinstance(col, np.uint8)):
                    self._initError()
        for row in rightImage:
            if not(isinstance(row, np.ndarray)):
                self._initError()
            for col in row:
                if not(isinstance(col, np.uint8)):
                    self._initError()

        if not(isinstance(leftTriangles, list)) or not(isinstance(rightTriangles, list)):
            self._initError()
        for tri in leftTriangles:
            if not(isinstance(tri, Triangle)):
                self._initError()
        for tri in rightTriangles:
            if not(isinstance(tri, Triangle)):
                self._initError()

        # size of image can be found using self.leftImage.shape
        self.leftImage = leftImage
        self.leftTriangles = leftTriangles
        self.rightImage = rightImage
        self.rightTriangles = rightTriangles

    def getImageAtAlpha(self, alpha):
        if alpha <= 0:
            return self.leftImage
        if alpha >= 1:
            return self.rightImage

        result = np.empty([self.leftImage.shape[0], self.leftImage.shape[1]], np.uint8)

        for tri_i in range(len(self.leftTriangles)):
            right_tri = self.rightTriangles[tri_i].vertices
            left_tri = self.leftTriangles[tri_i].vertices
            target_tri_vertices = alpha * right_tri + (1.0 - alpha) * left_tri
            target_tri = Triangle(target_tri_vertices)

            left_A = np.array([[left_tri[0][0], left_tri[0][1], 1, 0, 0, 0],
                               [0, 0, 0, left_tri[0][0], left_tri[0][1], 1],
                               [left_tri[1][0], left_tri[1][1], 1, 0, 0, 0],
                               [0, 0, 0, left_tri[1][0], left_tri[1][1], 1],
                               [left_tri[2][0], left_tri[2][1], 1, 0, 0, 0],
                               [0, 0, 0, left_tri[2][0], left_tri[2][1], 1]])
            right_A = np.array([[right_tri[0][0], right_tri[0][1], 1, 0, 0, 0],
                               [0, 0, 0, right_tri[0][0], right_tri[0][1], 1],
                               [right_tri[1][0], right_tri[1][1], 1, 0, 0, 0],
                               [0, 0, 0, right_tri[1][0], right_tri[1][1], 1],
                               [right_tri[2][0], right_tri[2][1], 1, 0, 0, 0],
                               [0, 0, 0, right_tri[2][0], right_tri[2][1], 1]])
            b = np.array([[target_tri_vertices[0][0]],
                          [target_tri_vertices[0][1]],
                          [target_tri_vertices[1][0]],
                          [target_tri_vertices[1][1]],
                          [target_tri_vertices[2][0]],
                          [target_tri_vertices[2][1]]])

            left_h_col = np.linalg.solve(left_A, b)
            right_h_col = np.linalg.solve(right_A, b)
            left_h = np.array([[left_h_col[0][0], left_h_col[1][0], left_h_col[2][0]],
                               [left_h_col[3][0], left_h_col[4][0], left_h_col[5][0]],
                               [0, 0, 1]])
            right_h = np.array([[right_h_col[0][0], right_h_col[1][0], right_h_col[2][0]],
                                [right_h_col[3][0], right_h_col[4][0], right_h_col[5][0]],
                                [0, 0, 1]])

            points_list = target_tri.getPoints()
            for point in points_list:
                left_part = np.linalg.solve(left_h, np.array([[point[0]], [point[1]], [1]]))
                right_part = np.linalg.solve(right_h, np.array([[point[0]], [point[1]], [1]]))
                result[int(point[1] ), int(point[0])] = np.uint8(np.round(\
                    (1.0 - alpha) * self.leftImage[int(np.round(left_part[1][0]))][int(np.round(left_part[0][0]))] + \
                    alpha * self.rightImage[int(np.round(right_part[1][0]))][int(np.round(right_part[0][0]))]))
        return result

'''
# TODO FIXME remember to delete all of this or at least comment it out
DataPath = os.path.expanduser('~ee364f17/Documents/labs-foogledoogle/Lab12/') # FIXME remember to delete
triangles = loadTriangles(DataPath + 'TestData/LeftGray.png.txt', DataPath + 'TestData/RightGray.png.txt')

im1 = np.array(imageio.imread(DataPath + 'TestData/LeftGray.png'))
im2 = np.array(imageio.imread(DataPath + 'TestData/RightGray.png'))

c = Morpher(im1, triangles[0], im2, triangles[1])

res = c.getImageAtAlpha(0.5)

imageio.imwrite(DataPath + 'ResultImage.png', res)

'''

'''
D = np.array([np.array([0.92, 2.12]), np.array([3.92, 5.12333]), np.array([6.23, -0.23])])
t = Triangle(D)
print(t.getPoints())'''
