#######################################################
#   Author:     Calvin Walter Heintzelman
#   email:      cheintze@purdue.edu
#   ID:         ee364f17
#   Date:       4/19/2019
#######################################################

import sys
import os
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter
from MorphingGUI import *
from Morphing import *
import numpy as np
import imageio
from scipy.spatial import Delaunay

#######################################################

class Morph(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Morph, self).__init__(parent)
        self.setupUi(self)

        self.type = 0 # 0 is both pictures have a text file, 1 is neither do, 2 is they do, but points were added
        self.temp_coord1 = None
        self.temp_coord2 = None
        self.start_normal_pixmap = None
        self.end_normal_pixmap = None
        self.start_clicked = False
        self.end_clicked = False
        self.start_im_pixels = None
        self.end_im_pixels = None
        self.triangles = (None, None)
        self.start_point_file = ""
        self.end_point_file = ""
        self.alpha = 0.0
        self.file1_loaded = False
        self.file2_loaded = False


        self.startIm.setStyleSheet("QLabel { background-color : white; }")
        self.endIm.setStyleSheet("QLabel { background-color : white; }")
        self.morphIm.setStyleSheet("QLabel { background-color : white; }")

        self.showTri.setEnabled(False)
        self.textEdit.setEnabled(False)
        self.slider.setEnabled(False)
        self.Blend.setEnabled(False)

        self.loadStart.clicked.connect(self.getImageFile1)
        self.loadEnd.clicked.connect(self.getImageFile2)

        self.slider.valueChanged.connect(self.test)
        self.showTri.stateChanged.connect(self.TriangleShow)

        self.Blend.clicked.connect(self.blender)

    def lastTris(self, leftPointFilePath, rightPointFilePath):
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

        r_points = []
        while r_line != '':
            r_points.append([np.float64(r_line[0:8]), np.float64(r_line[8:16])])
            r_line = r_file.readline()

        if not([np.float64(0.0), np.float64(0.0)] in l_points):
            l_points.append([np.float64(0.0), np.float64(0.0)])
            r_points.append([np.float64(0.0), np.float64(0.0)])
        if not([np.float64(self.start_im_pixels.shape[1] - 1.0), np.float64(0.0)] in l_points):
            l_points.append([np.float64(self.start_im_pixels.shape[1] - 1.0), np.float64(0.0)])
            r_points.append([np.float64(self.start_im_pixels.shape[1] - 1.0), np.float64(0.0)])
        if not([np.float64(0.0), np.float64(self.start_im_pixels.shape[0] - 1)] in l_points):
            l_points.append([np.float64(0.0), np.float64(self.start_im_pixels.shape[0] - 1.0)])
            r_points.append([np.float64(0.0), np.float64(self.start_im_pixels.shape[0] - 1.0)])
        if not([np.float64(self.start_im_pixels.shape[1] - 1.0), np.float64(self.start_im_pixels.shape[0] - 1)] in l_points):
            l_points.append([np.float64(self.start_im_pixels.shape[1] - 1.0), np.float64(self.start_im_pixels.shape[0] - 1.0)])
            r_points.append([np.float64(self.start_im_pixels.shape[1] - 1.0), np.float64(self.start_im_pixels.shape[0] - 1.0)])

        l_points = np.array(l_points)
        if len(l_points) < 3:
            return ([], [])
        l_tris = Delaunay(l_points)
        leftTriangles = []
        for triangle in l_points[l_tris.simplices]:
            leftTriangles.append(Triangle(triangle))

        r_points = np.array(r_points)
        rightTriangles = []
        for triangle in r_points[l_tris.simplices]:
            rightTriangles.append(Triangle(triangle))

        l_file.close()
        r_file.close()

        return (leftTriangles, rightTriangles)

    def blender(self):
        print("Waiting...")
        new_tris = self.lastTris(self.start_point_file, self.end_point_file)
        blend_class = Morpher(self.start_im_pixels, new_tris[0], self.end_im_pixels, new_tris[1])
        result = blend_class.getImageAtAlpha(float(self.slider.value()) / 1000)
        imageio.imwrite('ResultImage.png', result)
        pixmap = QPixmap('ResultImage.png')
        print("Done!")
        self.morphIm.setPixmap(pixmap.scaled(360, 270, Qt.KeepAspectRatio))
        self.file1_loaded = False
        self.file2_loaded = False


    def keyPressEvent(self, key: QtGui.QKeyEvent):
        if key.key() == QtCore.Qt.Key_Backspace and self.start_clicked is True:
            if self.end_clicked is False:
                self.start_clicked = False
                if self.showTri.isChecked() is True:
                    self.startIm.setPixmap(self.start_pixmap.scaled(360, 270, Qt.KeepAspectRatio))
                else:
                    self.startIm.setPixmap(self.start_normal_pixmap.scaled(360, 270, Qt.KeepAspectRatio))
            else:
                self.end_clicked = False
                if self.showTri.isChecked() is True:
                    self.endIm.setPixmap(self.end_pixmap.scaled(360, 270, Qt.KeepAspectRatio))
                else:
                    self.endIm.setPixmap(self.end_normal_pixmap.scaled(360, 270, Qt.KeepAspectRatio))

    def mousePressEvent(self, click: QtGui.QMouseEvent):
        if self.start_point_file != "" and self.end_point_file != "":
            x = click.pos().x()
            y = click.pos().y()
            if self.start_clicked is True and self.end_clicked is True and \
                    not(x >= 495 and x <= 855 and y >= 50 and y <= 320):
                if self.type == 0:
                    self.type = 2
                self.start_clicked = False
                self.end_clicked = False
                s_pixmap = self.start_normal_pixmap
                e_pixmap = self.end_normal_pixmap

                # draw on startIM
                painter = QPainter()
                painter.begin(s_pixmap)
                pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
                pen.setWidth(10)
                painter.setPen(pen)
                painter.drawEllipse(self.temp_coord1[0]-4, self.temp_coord1[1]-4, 10, 10)
                painter.end()
                self.startIm.setPixmap(s_pixmap.scaled(360, 270, Qt.KeepAspectRatio))

                # draw on endIM
                painter = QPainter()
                painter.begin(e_pixmap)
                pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
                pen.setWidth(10)
                painter.setPen(pen)
                painter.drawEllipse(self.temp_coord2[0]-4, self.temp_coord2[1]-4, 10, 10)
                painter.end()
                self.endIm.setPixmap(e_pixmap.scaled(360, 270, Qt.KeepAspectRatio))

                # write to files
                s_x = str(float(self.temp_coord1[0]))
                s_y = str(float(self.temp_coord1[1]))
                e_x = str(float(self.temp_coord2[0]))
                e_y = str(float(self.temp_coord2[1]))
                s_str = (8 - len(s_x))*" " + s_x + (8 - len(s_y))*" " + s_y
                e_str = (8 - len(e_x))*" " + e_x + (8 - len(e_y))*" " + e_y
                if os.stat(self.start_point_file).st_size != 0:
                    s_str = '\n' + s_str
                if os.stat(self.end_point_file).st_size != 0:
                    e_str = '\n' + e_str
                f = open(self.start_point_file, 'a+')
                f.write(s_str)
                f.close()
                f = open(self.end_point_file, 'a+')
                f.write(e_str)
                f.close()
                self.triangles = loadTriangles(self.start_point_file, self.end_point_file)
                if self.showTri.isChecked():
                    self.TriangleShow()

            y_to_x_ratio = self.start_im_pixels.shape[0] / self.start_im_pixels.shape[1]
            x_l = self.start_im_pixels.shape[1]
            y_l = self.start_im_pixels.shape[0]
            if y_to_x_ratio <= 3.0/4.0:
                x_compare = 360
                y_compare = y_to_x_ratio * 360.0 # 180 or 90
            else:
                x_compare = 1.0/y_to_x_ratio * 270.0
                y_compare = 0

            if x > 45 and x < 45 + x_compare and y > 50 + y_compare and y < 320 - y_compare: # start image
                if y_to_x_ratio <= 3.0/4.0:
                    x_pos = np.round((x - 45.0) * x_l/360.0)
                    y_pos = np.round((y - 50 - y_compare))
                else:
                    x_pos = np.round((x - 45.0) * y_l/270.0)
                    y_pos = np.round((y - 50.0) * y_l/270)
                if x_pos >= self.start_im_pixels.shape[1]:
                    x_pos -= 1
                if y_pos >= self.start_im_pixels.shape[0]:
                    y_pos -= 1

                if self.start_clicked is False:
                    self.start_clicked = True
                    self.temp_coord1 = (x_pos, y_pos)
                    if self.showTri.isChecked() is True:
                        s_pixmap = self.start_pixmap.copy()
                    else:
                        s_pixmap = self.start_normal_pixmap.copy()
                    painter = QPainter()
                    painter.begin(s_pixmap)
                    pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
                    pen.setWidth(10)
                    painter.setPen(pen)
                    painter.drawEllipse(x_pos-4, y_pos-4, 10, 10)
                    painter.end()
                    self.startIm.setPixmap(s_pixmap.scaled(360, 270, Qt.KeepAspectRatio))

            if x > 495 and x < 495 + x_compare and y > 50 + y_compare and y < 320 - y_compare: # end image
                if y_to_x_ratio <= 3.0/4.0:
                    x_pos = np.round((x - 495.0) * x_l/360.0)
                    y_pos = np.round((y - 50 - y_compare))
                else:
                    x_pos = np.round((x - 495.0) * y_l/270.0)
                    y_pos = np.round((y - 50.0) * y_l/270)
                if y_pos == self.start_im_pixels.shape[0]:
                    y_pos -= 1
                if x_pos == self.start_im_pixels.shape[1]:
                    x_pos -= 1

                if self.start_clicked is True and self.end_clicked is False:
                    self.end_clicked = True
                    self.temp_coord2 = (x_pos, y_pos)
                    if self.showTri.isChecked() is True:
                        e_pixmap = self.end_pixmap.copy()
                    else:
                        e_pixmap = self.end_normal_pixmap.copy()
                    painter = QPainter()
                    painter.begin(e_pixmap)
                    pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
                    pen.setWidth(10)
                    painter.setPen(pen)
                    painter.drawEllipse(x_pos-4, y_pos-4, 10, 10)
                    painter.end()
                    self.endIm.setPixmap(e_pixmap.scaled(360, 270, Qt.KeepAspectRatio))

    def TriangleShow(self):
        if self.showTri.isChecked() is True:
            self.start_pixmap = self.start_normal_pixmap.copy()
            self.end_pixmap = self.end_normal_pixmap.copy()

            painter = QPainter()
            painter.begin(self.start_pixmap)
            if self.type == 0:
                pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
            elif self.type == 1:
                pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
            else:
                pen = QtGui.QPen(QtGui.QColor(0, 255, 255))
            pen.setWidth(4)
            painter.setPen(pen)
            for tri in self.triangles[0]:
                painter.drawLine(tri.vertices[0][0], tri.vertices[0][1], tri.vertices[1][0], tri.vertices[1][1])
                painter.drawLine(tri.vertices[2][0], tri.vertices[2][1], tri.vertices[1][0], tri.vertices[1][1])
                painter.drawLine(tri.vertices[0][0], tri.vertices[0][1], tri.vertices[2][0], tri.vertices[2][1])
            painter.end()

            s_pixmap = self.start_pixmap.copy()
            if self.start_clicked is True:
                painter = QPainter()
                painter.begin(s_pixmap)
                pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
                pen.setWidth(10)
                painter.setPen(pen)
                painter.drawEllipse(self.temp_coord1[0]-4, self.temp_coord1[1]-4, 10, 10)
                painter.end()

            painter = QPainter()
            painter.begin(self.end_pixmap)
            if self.type == 0:
                pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
            elif self.type == 1:
                pen = QtGui.QPen(QtGui.QColor(0, 0, 255))
            else:
                pen = QtGui.QPen(QtGui.QColor(0, 255, 255))
            pen.setWidth(4)
            painter.setPen(pen)
            for tri in self.triangles[1]:
                painter.drawLine(tri.vertices[0][0], tri.vertices[0][1], tri.vertices[1][0], tri.vertices[1][1])
                painter.drawLine(tri.vertices[2][0], tri.vertices[2][1], tri.vertices[1][0], tri.vertices[1][1])
                painter.drawLine(tri.vertices[0][0], tri.vertices[0][1], tri.vertices[2][0], tri.vertices[2][1])
            painter.end()

            e_pixmap = self.end_pixmap.copy()
            if self.end_clicked is True:
                painter = QPainter()
                painter.begin(e_pixmap)
                pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
                pen.setWidth(10)
                painter.setPen(pen)
                painter.drawEllipse(self.temp_coord2[0]-4, self.temp_coord2[1]-4, 10, 10)
                painter.end()

            self.startIm.setPixmap(s_pixmap.scaled(360, 270, Qt.KeepAspectRatio))
            self.endIm.setPixmap(e_pixmap.scaled(360, 270, Qt.KeepAspectRatio))
        else:
            s_pixmap = self.start_normal_pixmap.copy()
            if self.start_clicked is True:
                painter = QPainter()
                painter.begin(s_pixmap)
                pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
                pen.setWidth(10)
                painter.setPen(pen)
                painter.drawEllipse(self.temp_coord1[0]-4, self.temp_coord1[1]-4, 10, 10)
                painter.end()

            e_pixmap = self.end_normal_pixmap.copy()
            if self.end_clicked is True:
                painter = QPainter()
                painter.begin(e_pixmap)
                pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
                pen.setWidth(10)
                painter.setPen(pen)
                painter.drawEllipse(self.temp_coord2[0]-4, self.temp_coord2[1]-4, 10, 10)
                painter.end()

            self.startIm.setPixmap(s_pixmap.scaled(360, 270, Qt.KeepAspectRatio))
            self.endIm.setPixmap(e_pixmap.scaled(360, 270, Qt.KeepAspectRatio))

    def test(self):
        self.alpha = float(self.slider.value() / 1000.0)
        self.textEdit.setText(str(float(self.slider.value()) / 1000.0))
        self.textEdit.setAlignment(Qt.AlignCenter)

    def makeTriangles(self):
        if self.file1_loaded and self.file2_loaded:
            self.triangles = loadTriangles(self.start_point_file, self.end_point_file)
            self.showTri.setEnabled(True)
            self.textEdit.setEnabled(True)
            self.slider.setEnabled(True)
            self.Blend.setEnabled(True)
            self.TriangleShow()
            self.file1_loaded = False
            self.file2_loaded = False

    def getImageFile1(self):
        filePath, _ = QFileDialog.getOpenFileName\
            (self, caption='Open image file ...', filter="PNG image (*.png *.jpg)")

        if not filePath:
            return

        self.start_im_pixels = np.array(imageio.imread(filePath))
        self.start_point_file = filePath + ".txt"

        if not(os.path.isfile(self.start_point_file)):
            f = open(self.start_point_file, 'w')
            f.close()

        if os.stat(self.start_point_file).st_size == 0:
            self.type = 1
        else:
            self.type = 0

        f = open(self.start_point_file, 'r')
        l = f.readline()
        self.start_points = []
        while l != '':
            self.start_points.append([np.float64(l[0:8]), np.float64(l[8:16])])
            l = f.readline()
        f.close()

        pixmap = QPixmap(filePath)
        painter = QPainter()
        painter.begin(pixmap)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        pen.setWidth(10)
        painter.setPen(pen)
        for point in self.start_points:
            painter.drawEllipse(round(point[0])-4, round(point[1])-4, 10, 10)
        painter.end()

        self.start_normal_pixmap = pixmap
        self.startIm.setPixmap(pixmap.scaled(360, 270, Qt.KeepAspectRatio))

        self.file1_loaded = True

        self.makeTriangles()

    def getImageFile2(self):
        filePath, _ = QFileDialog.getOpenFileName\
            (self, caption='Open image file ...', filter="PNG image (*.png *.jpg)")

        if not filePath:
            return

        self.end_im_pixels = np.array(imageio.imread(filePath))
        self.end_point_file = filePath + ".txt"

        if not(os.path.isfile(self.end_point_file)):
            f = open(self.end_point_file, 'w')
            f.close()

        if os.stat(self.end_point_file).st_size == 0:
            self.type = 1

        f = open(self.end_point_file, 'r')
        l = f.readline()
        self.end_points = []
        while l != '':
            self.end_points.append([np.float64(l[0:8]), np.float64(l[8:16])])
            l = f.readline()
        f.close()

        pixmap = QPixmap(filePath)
        painter = QPainter()
        painter.begin(pixmap)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
        pen.setWidth(10)
        painter.setPen(pen)
        for point in self.end_points:
            painter.drawEllipse(round(point[0])-4, round(point[1])-4, 10, 10)
        painter.end()

        self.end_normal_pixmap = pixmap
        self.endIm.setPixmap(pixmap.scaled(360, 270, Qt.KeepAspectRatio))

        self.file2_loaded = True

        self.makeTriangles()

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Morph()

    currentForm.show()
    currentApp.exec_()
