# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SubWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SubWindow(object):
    def setupUi(self, SubWindow):
        SubWindow.setObjectName("SubWindow")
        SubWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(SubWindow)
        self.centralwidget.setObjectName("centralwidget")
        SubWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SubWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        SubWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SubWindow)
        self.statusbar.setObjectName("statusbar")
        SubWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SubWindow)
        QtCore.QMetaObject.connectSlotsByName(SubWindow)

    def retranslateUi(self, SubWindow):
        _translate = QtCore.QCoreApplication.translate
        SubWindow.setWindowTitle(_translate("SubWindow", "MainWindow"))

