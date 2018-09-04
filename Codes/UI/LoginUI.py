# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT_UI/Login.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(215, 180)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginWindow.sizePolicy().hasHeightForWidth())
        LoginWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoginWindow.setWindowIcon(icon)
        LoginWindow.setWhatsThis("")
        self.QLoginWindow = QtWidgets.QWidget(LoginWindow)
        self.QLoginWindow.setGeometry(QtCore.QRect(0, 0, 215, 180))
        self.QLoginWindow.setObjectName("QLoginWindow")
        self.Label_User = QtWidgets.QLabel(self.QLoginWindow)
        self.Label_User.setGeometry(QtCore.QRect(20, 20, 50, 20))
        self.Label_User.setObjectName("Label_User")
        self.Label_ShowUser = QtWidgets.QLabel(self.QLoginWindow)
        self.Label_ShowUser.setGeometry(QtCore.QRect(75, 20, 120, 20))
        self.Label_ShowUser.setWhatsThis("")
        self.Label_ShowUser.setTextFormat(QtCore.Qt.AutoText)
        self.Label_ShowUser.setObjectName("Label_ShowUser")
        self.Label_Psw = QtWidgets.QLabel(self.QLoginWindow)
        self.Label_Psw.setGeometry(QtCore.QRect(20, 50, 35, 20))
        self.Label_Psw.setObjectName("Label_Psw")
        self.Text_Psw = QtWidgets.QLineEdit(self.QLoginWindow)
        self.Text_Psw.setGeometry(QtCore.QRect(75, 50, 120, 20))
        self.Text_Psw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Text_Psw.setObjectName("Text_Psw")
        self.Check_NoPsw = QtWidgets.QCheckBox(self.QLoginWindow)
        self.Check_NoPsw.setGeometry(QtCore.QRect(20, 80, 120, 20))
        self.Check_NoPsw.setObjectName("Check_NoPsw")
        self.Label_Status = QtWidgets.QLabel(self.QLoginWindow)
        self.Label_Status.setGeometry(QtCore.QRect(20, 110, 95, 25))
        self.Label_Status.setObjectName("Label_Status")
        self.Btn_Login = QtWidgets.QPushButton(self.QLoginWindow)
        self.Btn_Login.setGeometry(QtCore.QRect(120, 110, 75, 25))
        self.Btn_Login.setObjectName("Btn_Login")
        self.Tool_Close = QtWidgets.QToolButton(self.QLoginWindow)
        self.Tool_Close.setGeometry(QtCore.QRect(185, 0, 20, 20))
        self.Tool_Close.setText("")
        self.Tool_Close.setObjectName("Tool_Close")
        self.Tool_Min = QtWidgets.QToolButton(self.QLoginWindow)
        self.Tool_Min.setGeometry(QtCore.QRect(165, 0, 20, 20))
        self.Tool_Min.setText("")
        self.Tool_Min.setObjectName("Tool_Min")

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
        LoginWindow.setTabOrder(self.Text_Psw, self.Check_NoPsw)
        LoginWindow.setTabOrder(self.Check_NoPsw, self.Btn_Login)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "登录"))
        self.Label_User.setText(_translate("LoginWindow", "用户名："))
        self.Label_Psw.setText(_translate("LoginWindow", "密码："))
        self.Check_NoPsw.setText(_translate("LoginWindow", "下次直接登录"))
        self.Btn_Login.setText(_translate("LoginWindow", "登录"))

