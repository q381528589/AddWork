# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChgPsw.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(240, 160)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.Label_OldPsw = QtWidgets.QLabel(Form)
        self.Label_OldPsw.setGeometry(QtCore.QRect(20, 15, 60, 16))
        self.Label_OldPsw.setObjectName("Label_OldPsw")
        self.Text_OldPsw = QtWidgets.QLineEdit(Form)
        self.Text_OldPsw.setGeometry(QtCore.QRect(88, 15, 135, 20))
        self.Text_OldPsw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_OldPsw.setObjectName("Text_OldPsw")
        self.Label_NewPsw = QtWidgets.QLabel(Form)
        self.Label_NewPsw.setGeometry(QtCore.QRect(20, 50, 60, 16))
        self.Label_NewPsw.setObjectName("Label_NewPsw")
        self.Text_NewPsw = QtWidgets.QLineEdit(Form)
        self.Text_NewPsw.setGeometry(QtCore.QRect(88, 50, 135, 20))
        self.Text_NewPsw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_NewPsw.setObjectName("Text_NewPsw")
        self.Label_CheckPsw = QtWidgets.QLabel(Form)
        self.Label_CheckPsw.setGeometry(QtCore.QRect(20, 85, 60, 16))
        self.Label_CheckPsw.setObjectName("Label_CheckPsw")
        self.Text_CheckPsw = QtWidgets.QLineEdit(Form)
        self.Text_CheckPsw.setGeometry(QtCore.QRect(88, 85, 135, 20))
        self.Text_CheckPsw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_CheckPsw.setObjectName("Text_CheckPsw")
        self.Btn_OK = QtWidgets.QPushButton(Form)
        self.Btn_OK.setGeometry(QtCore.QRect(70, 120, 72, 23))
        self.Btn_OK.setObjectName("Btn_OK")
        self.Btn_Clear = QtWidgets.QPushButton(Form)
        self.Btn_Clear.setGeometry(QtCore.QRect(148, 120, 72, 23))
        self.Btn_Clear.setObjectName("Btn_Clear")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "修改密码"))
        self.Label_OldPsw.setText(_translate("Form", "原密码："))
        self.Label_NewPsw.setText(_translate("Form", "新密码："))
        self.Label_CheckPsw.setText(_translate("Form", "确认密码："))
        self.Btn_OK.setText(_translate("Form", "确认更改"))
        self.Btn_Clear.setText(_translate("Form", "重置"))

