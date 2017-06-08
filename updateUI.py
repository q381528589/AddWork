# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'update.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(227, 94)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(20, 20, 191, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 191, 16))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(50, 50, 158, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Btn_OK = QtWidgets.QPushButton(self.widget)
        self.Btn_OK.setObjectName("Btn_OK")
        self.horizontalLayout.addWidget(self.Btn_OK)
        self.Btn_Cancel = QtWidgets.QPushButton(self.widget)
        self.Btn_Cancel.setObjectName("Btn_Cancel")
        self.horizontalLayout.addWidget(self.Btn_Cancel)

        self.retranslateUi(Dialog)
        self.Btn_Cancel.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "自动更新"))
        self.label.setText(_translate("Dialog", "发现新版本：2.0.4.34，是否更新？"))
        self.Btn_OK.setText(_translate("Dialog", "OK"))
        self.Btn_Cancel.setText(_translate("Dialog", "Cancel"))

