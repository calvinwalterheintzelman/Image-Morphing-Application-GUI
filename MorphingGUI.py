# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Blend = QtWidgets.QPushButton(self.centralwidget)
        self.Blend.setGeometry(QtCore.QRect(400, 750, 100, 26))
        self.Blend.setObjectName("Blend")
        self.loadStart = QtWidgets.QPushButton(self.centralwidget)
        self.loadStart.setGeometry(QtCore.QRect(45, 10, 171, 31))
        self.loadStart.setObjectName("loadStart")
        self.showTri = QtWidgets.QCheckBox(self.centralwidget)
        self.showTri.setGeometry(QtCore.QRect(390, 360, 120, 22))
        self.showTri.setAutoFillBackground(False)
        self.showTri.setCheckable(True)
        self.showTri.setChecked(False)
        self.showTri.setTristate(False)
        self.showTri.setObjectName("showTri")
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setEnabled(True)
        self.slider.setGeometry(QtCore.QRect(150, 390, 600, 25))
        self.slider.setMinimumSize(QtCore.QSize(591, 0))
        self.slider.setMouseTracking(False)
        self.slider.setAcceptDrops(False)
        self.slider.setAutoFillBackground(True)
        self.slider.setMaximum(1000)
        self.slider.setSingleStep(50)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setInvertedAppearance(False)
        self.slider.setInvertedControls(False)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.setTickInterval(100)
        self.slider.setObjectName("slider")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(760, 390, 81, 28))
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.loadEnd = QtWidgets.QPushButton(self.centralwidget)
        self.loadEnd.setGeometry(QtCore.QRect(495, 10, 171, 31))
        self.loadEnd.setObjectName("loadEnd")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 390, 41, 16))
        self.label.setObjectName("label")
        self.startIm = QtWidgets.QLabel(self.centralwidget)
        self.startIm.setGeometry(QtCore.QRect(45, 50, 360, 270))
        self.startIm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.startIm.setFrameShadow(QtWidgets.QFrame.Plain)
        self.startIm.setText("")
        self.startIm.setObjectName("startIm")
        self.endIm = QtWidgets.QLabel(self.centralwidget)
        self.endIm.setGeometry(QtCore.QRect(495, 50, 360, 270))
        self.endIm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.endIm.setFrameShadow(QtWidgets.QFrame.Plain)
        self.endIm.setText("")
        self.endIm.setObjectName("endIm")
        self.morphIm = QtWidgets.QLabel(self.centralwidget)
        self.morphIm.setGeometry(QtCore.QRect(270, 435, 360, 270))
        self.morphIm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.morphIm.setFrameShadow(QtWidgets.QFrame.Plain)
        self.morphIm.setText("")
        self.morphIm.setObjectName("morphIm")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(135, 330, 180, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(585, 330, 180, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(380, 715, 140, 22))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(150, 420, 31, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(730, 420, 21, 16))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Blend.setText(_translate("MainWindow", "Blend"))
        self.loadStart.setText(_translate("MainWindow", "Load Starting Image ..."))
        self.showTri.setText(_translate("MainWindow", "Show Triangles"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.0</p></body></html>"))
        self.loadEnd.setText(_translate("MainWindow", "Load Ending Image ..."))
        self.label.setText(_translate("MainWindow", "Alpha"))
        self.label_2.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Starting Image</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Ending Image</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Blending Image</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">0.0</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">1.0</span></p></body></html>"))

