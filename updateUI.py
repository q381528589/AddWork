# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'update.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UpdateWindow(object):
    def setupUi(self, UpdateWindow):
        UpdateWindow.setObjectName("UpdateWindow")
        UpdateWindow.resize(283, 108)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UpdateWindow.sizePolicy().hasHeightForWidth())
        UpdateWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(UpdateWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Btn_OK = QtWidgets.QPushButton(self.centralwidget)
        self.Btn_OK.setGeometry(QtCore.QRect(186, 67, 75, 23))
        self.Btn_OK.setObjectName("Btn_OK")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 19, 251, 40))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Label_Status = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_Status.sizePolicy().hasHeightForWidth())
        self.Label_Status.setSizePolicy(sizePolicy)
        self.Label_Status.setObjectName("Label_Status")
        self.verticalLayout.addWidget(self.Label_Status)
        self.Bar_Status = QtWidgets.QProgressBar(self.widget)
        self.Bar_Status.setProperty("value", 24)
        self.Bar_Status.setObjectName("Bar_Status")
        self.verticalLayout.addWidget(self.Bar_Status)
        UpdateWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(UpdateWindow)
        QtCore.QMetaObject.connectSlotsByName(UpdateWindow)

    def retranslateUi(self, UpdateWindow):
        _translate = QtCore.QCoreApplication.translate
        UpdateWindow.setWindowTitle(_translate("UpdateWindow", "程序更新"))
        self.Btn_OK.setText(_translate("UpdateWindow", "完成"))
        self.Label_Status.setText(_translate("UpdateWindow", "TextLabel"))

