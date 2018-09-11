# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT_UI/About.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(520, 250)
        self.Label_Title = QtWidgets.QLabel(About)
        self.Label_Title.setGeometry(QtCore.QRect(10, 0, 200, 20))
        self.Label_Title.setObjectName("Label_Title")
        self.Label_Pixmap = QtWidgets.QLabel(About)
        self.Label_Pixmap.setGeometry(QtCore.QRect(210, 30, 100, 105))
        self.Label_Pixmap.setText("")
        self.Label_Pixmap.setPixmap(QtGui.QPixmap("./Icon.png"))
        self.Label_Pixmap.setScaledContents(True)
        self.Label_Pixmap.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_Pixmap.setObjectName("Label_Pixmap")
        self.Label_Version = QtWidgets.QLabel(About)
        self.Label_Version.setGeometry(QtCore.QRect(190, 160, 140, 20))
        self.Label_Version.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_Version.setObjectName("Label_Version")
        self.Label_Copyright = QtWidgets.QLabel(About)
        self.Label_Copyright.setGeometry(QtCore.QRect(100, 190, 320, 20))
        self.Label_Copyright.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_Copyright.setObjectName("Label_Copyright")
        self.Tool_Close = QtWidgets.QToolButton(About)
        self.Tool_Close.setGeometry(QtCore.QRect(495, 0, 20, 20))
        self.Tool_Close.setText("")
        self.Tool_Close.setObjectName("Tool_Close")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "Dialog"))
        self.Label_Title.setText(_translate("About", "一键加班应用程序"))
        self.Label_Version.setText(_translate("About", "软件版本: 0.0.0.000"))
        self.Label_Copyright.setText(_translate("About", "Copyright (C) 1995-2018 Synway. All Rights Reserved."))

