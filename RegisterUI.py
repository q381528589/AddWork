# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Register.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CRegister(object):
    def setupUi(self, CRegister):
        CRegister.setObjectName("CRegister")
        CRegister.resize(262, 288)
        self.Label_User = QtWidgets.QLabel(CRegister)
        self.Label_User.setGeometry(QtCore.QRect(21, 18, 64, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_User.setFont(font)
        self.Label_User.setObjectName("Label_User")
        self.Lablel_Psw1 = QtWidgets.QLabel(CRegister)
        self.Lablel_Psw1.setGeometry(QtCore.QRect(21, 50, 48, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Lablel_Psw1.setFont(font)
        self.Lablel_Psw1.setObjectName("Lablel_Psw1")
        self.Label_Psw2 = QtWidgets.QLabel(CRegister)
        self.Label_Psw2.setGeometry(QtCore.QRect(21, 82, 80, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_Psw2.setFont(font)
        self.Label_Psw2.setObjectName("Label_Psw2")
        self.Label_Dinner = QtWidgets.QLabel(CRegister)
        self.Label_Dinner.setGeometry(QtCore.QRect(21, 146, 64, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_Dinner.setFont(font)
        self.Label_Dinner.setObjectName("Label_Dinner")
        self.Label_Bus = QtWidgets.QLabel(CRegister)
        self.Label_Bus.setGeometry(QtCore.QRect(21, 178, 80, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_Bus.setFont(font)
        self.Label_Bus.setObjectName("Label_Bus")
        self.Text_User = QtWidgets.QLineEdit(CRegister)
        self.Text_User.setGeometry(QtCore.QRect(107, 18, 133, 23))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Text_User.setFont(font)
        self.Text_User.setObjectName("Text_User")
        self.Text_Psw1 = QtWidgets.QLineEdit(CRegister)
        self.Text_Psw1.setGeometry(QtCore.QRect(107, 50, 133, 23))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Text_Psw1.setFont(font)
        self.Text_Psw1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_Psw1.setObjectName("Text_Psw1")
        self.Text_Psw2 = QtWidgets.QLineEdit(CRegister)
        self.Text_Psw2.setGeometry(QtCore.QRect(107, 82, 133, 23))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Text_Psw2.setFont(font)
        self.Text_Psw2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_Psw2.setObjectName("Text_Psw2")
        self.Combo_Dinner = QtWidgets.QComboBox(CRegister)
        self.Combo_Dinner.setGeometry(QtCore.QRect(107, 146, 131, 23))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Combo_Dinner.setFont(font)
        self.Combo_Dinner.setObjectName("Combo_Dinner")
        self.Combo_Dinner.addItem("")
        self.Combo_Dinner.addItem("")
        self.Combo_Bus = QtWidgets.QComboBox(CRegister)
        self.Combo_Bus.setGeometry(QtCore.QRect(107, 178, 131, 23))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Combo_Bus.setFont(font)
        self.Combo_Bus.setObjectName("Combo_Bus")
        self.Combo_Bus.addItem("")
        self.Combo_Bus.addItem("")
        self.Text_Reason = QtWidgets.QLineEdit(CRegister)
        self.Text_Reason.setGeometry(QtCore.QRect(107, 210, 133, 23))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Text_Reason.setFont(font)
        self.Text_Reason.setObjectName("Text_Reason")
        self.Btn_Regist = QtWidgets.QPushButton(CRegister)
        self.Btn_Regist.setGeometry(QtCore.QRect(165, 242, 75, 26))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Btn_Regist.setFont(font)
        self.Btn_Regist.setObjectName("Btn_Regist")
        self.Text_RegCode = QtWidgets.QLineEdit(CRegister)
        self.Text_RegCode.setGeometry(QtCore.QRect(107, 114, 133, 23))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Text_RegCode.setFont(font)
        self.Text_RegCode.setObjectName("Text_RegCode")
        self.Label_RegCode = QtWidgets.QLabel(CRegister)
        self.Label_RegCode.setGeometry(QtCore.QRect(21, 114, 48, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_RegCode.setFont(font)
        self.Label_RegCode.setObjectName("Label_RegCode")
        self.Label_Reason = QtWidgets.QLabel(CRegister)
        self.Label_Reason.setGeometry(QtCore.QRect(21, 210, 80, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_Reason.setFont(font)
        self.Label_Reason.setObjectName("Label_Reason")
        self.Label_Status = QtWidgets.QLabel(CRegister)
        self.Label_Status.setGeometry(QtCore.QRect(21, 242, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.Label_Status.setFont(font)
        self.Label_Status.setText("")
        self.Label_Status.setObjectName("Label_Status")

        self.retranslateUi(CRegister)
        QtCore.QMetaObject.connectSlotsByName(CRegister)
        CRegister.setTabOrder(self.Text_User, self.Text_Psw1)
        CRegister.setTabOrder(self.Text_Psw1, self.Text_Psw2)
        CRegister.setTabOrder(self.Text_Psw2, self.Text_RegCode)
        CRegister.setTabOrder(self.Text_RegCode, self.Combo_Dinner)
        CRegister.setTabOrder(self.Combo_Dinner, self.Combo_Bus)
        CRegister.setTabOrder(self.Combo_Bus, self.Text_Reason)
        CRegister.setTabOrder(self.Text_Reason, self.Btn_Regist)

    def retranslateUi(self, CRegister):
        _translate = QtCore.QCoreApplication.translate
        CRegister.setWindowTitle(_translate("CRegister", "注册"))
        self.Label_User.setText(_translate("CRegister", "用户名："))
        self.Lablel_Psw1.setText(_translate("CRegister", "密码："))
        self.Label_Psw2.setText(_translate("CRegister", "确认密码："))
        self.Label_Dinner.setText(_translate("CRegister", "加班餐："))
        self.Label_Bus.setText(_translate("CRegister", "加班班车："))
        self.Combo_Dinner.setItemText(0, _translate("CRegister", "是"))
        self.Combo_Dinner.setItemText(1, _translate("CRegister", "否"))
        self.Combo_Bus.setItemText(0, _translate("CRegister", "是"))
        self.Combo_Bus.setItemText(1, _translate("CRegister", "否"))
        self.Text_Reason.setText(_translate("CRegister", "加班"))
        self.Btn_Regist.setText(_translate("CRegister", "注册"))
        self.Label_RegCode.setText(_translate("CRegister", "注册码"))
        self.Label_Reason.setText(_translate("CRegister", "加班理由："))

