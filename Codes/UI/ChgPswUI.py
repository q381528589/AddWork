# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChgPsw.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChgPswWindow(object):
    def setupUi(self, ChgPswWindow):
        ChgPswWindow.setObjectName("ChgPswWindow")
        ChgPswWindow.resize(240, 160)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ChgPswWindow.sizePolicy().hasHeightForWidth())
        ChgPswWindow.setSizePolicy(sizePolicy)
        self.Label_OldPsw = QtWidgets.QLabel(ChgPswWindow)
        self.Label_OldPsw.setGeometry(QtCore.QRect(20, 15, 60, 16))
        self.Label_OldPsw.setObjectName("Label_OldPsw")
        self.Text_OldPsw = QtWidgets.QLineEdit(ChgPswWindow)
        self.Text_OldPsw.setGeometry(QtCore.QRect(88, 15, 135, 20))
        self.Text_OldPsw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_OldPsw.setObjectName("Text_OldPsw")
        self.Label_NewPsw = QtWidgets.QLabel(ChgPswWindow)
        self.Label_NewPsw.setGeometry(QtCore.QRect(20, 50, 60, 16))
        self.Label_NewPsw.setObjectName("Label_NewPsw")
        self.Text_NewPsw = QtWidgets.QLineEdit(ChgPswWindow)
        self.Text_NewPsw.setGeometry(QtCore.QRect(88, 50, 135, 20))
        self.Text_NewPsw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_NewPsw.setObjectName("Text_NewPsw")
        self.Label_CheckPsw = QtWidgets.QLabel(ChgPswWindow)
        self.Label_CheckPsw.setGeometry(QtCore.QRect(20, 85, 60, 16))
        self.Label_CheckPsw.setObjectName("Label_CheckPsw")
        self.Text_CheckPsw = QtWidgets.QLineEdit(ChgPswWindow)
        self.Text_CheckPsw.setGeometry(QtCore.QRect(88, 85, 135, 20))
        self.Text_CheckPsw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_CheckPsw.setObjectName("Text_CheckPsw")
        self.Btn_OK = QtWidgets.QPushButton(ChgPswWindow)
        self.Btn_OK.setGeometry(QtCore.QRect(70, 120, 72, 23))
        self.Btn_OK.setObjectName("Btn_OK")
        self.Btn_Clear = QtWidgets.QPushButton(ChgPswWindow)
        self.Btn_Clear.setGeometry(QtCore.QRect(148, 120, 72, 23))
        self.Btn_Clear.setObjectName("Btn_Clear")

        self.retranslateUi(ChgPswWindow)
        QtCore.QMetaObject.connectSlotsByName(ChgPswWindow)

    def retranslateUi(self, ChgPswWindow):
        _translate = QtCore.QCoreApplication.translate
        ChgPswWindow.setWindowTitle(_translate("ChgPswWindow", "修改密码"))
        self.Label_OldPsw.setText(_translate("ChgPswWindow", "原密码："))
        self.Label_NewPsw.setText(_translate("ChgPswWindow", "新密码："))
        self.Label_CheckPsw.setText(_translate("ChgPswWindow", "确认密码："))
        self.Btn_OK.setText(_translate("ChgPswWindow", "确认更改"))
        self.Btn_Clear.setText(_translate("ChgPswWindow", "重置"))

