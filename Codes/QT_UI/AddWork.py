# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddWork.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddWorkWindow(object):
    def setupUi(self, AddWorkWindow):
        AddWorkWindow.setObjectName("AddWorkWindow")
        AddWorkWindow.resize(374, 293)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddWorkWindow.sizePolicy().hasHeightForWidth())
        AddWorkWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AddWorkWindow.setWindowIcon(icon)
        self.CAddWork = QtWidgets.QWidget(AddWorkWindow)
        self.CAddWork.setObjectName("CAddWork")
        self.Label_User = QtWidgets.QLabel(self.CAddWork)
        self.Label_User.setGeometry(QtCore.QRect(180, 15, 70, 20))
        self.Label_User.setObjectName("Label_User")
        self.Label_CurUser = QtWidgets.QLabel(self.CAddWork)
        self.Label_CurUser.setGeometry(QtCore.QRect(235, 15, 80, 20))
        self.Label_CurUser.setObjectName("Label_CurUser")
        self.Label_Dinner = QtWidgets.QLabel(self.CAddWork)
        self.Label_Dinner.setGeometry(QtCore.QRect(20, 50, 60, 16))
        self.Label_Dinner.setObjectName("Label_Dinner")
        self.Label_Bus = QtWidgets.QLabel(self.CAddWork)
        self.Label_Bus.setGeometry(QtCore.QRect(20, 80, 60, 16))
        self.Label_Bus.setObjectName("Label_Bus")
        self.Label_Reason = QtWidgets.QLabel(self.CAddWork)
        self.Label_Reason.setGeometry(QtCore.QRect(20, 110, 60, 16))
        self.Label_Reason.setObjectName("Label_Reason")
        self.Edit_Status = QtWidgets.QPlainTextEdit(self.CAddWork)
        self.Edit_Status.setGeometry(QtCore.QRect(20, 140, 330, 120))
        self.Edit_Status.setReadOnly(True)
        self.Edit_Status.setObjectName("Edit_Status")
        self.Edit_Reason = QtWidgets.QLineEdit(self.CAddWork)
        self.Edit_Reason.setGeometry(QtCore.QRect(90, 110, 260, 20))
        self.Edit_Reason.setObjectName("Edit_Reason")
        self.Combo_Dinner = QtWidgets.QComboBox(self.CAddWork)
        self.Combo_Dinner.setGeometry(QtCore.QRect(90, 50, 70, 20))
        self.Combo_Dinner.setObjectName("Combo_Dinner")
        self.Combo_Dinner.addItem("")
        self.Combo_Dinner.addItem("")
        self.Combo_Bus = QtWidgets.QComboBox(self.CAddWork)
        self.Combo_Bus.setGeometry(QtCore.QRect(90, 80, 70, 20))
        self.Combo_Bus.setObjectName("Combo_Bus")
        self.Combo_Bus.addItem("")
        self.Combo_Bus.addItem("")
        self.Btn_AddWork = QtWidgets.QPushButton(self.CAddWork)
        self.Btn_AddWork.setGeometry(QtCore.QRect(275, 50, 75, 50))
        self.Btn_AddWork.setObjectName("Btn_AddWork")
        self.toolButton = QtWidgets.QToolButton(self.CAddWork)
        self.toolButton.setGeometry(QtCore.QRect(325, 10, 25, 25))
        self.toolButton.setObjectName("toolButton")
        AddWorkWindow.setCentralWidget(self.CAddWork)

        self.retranslateUi(AddWorkWindow)
        QtCore.QMetaObject.connectSlotsByName(AddWorkWindow)
        AddWorkWindow.setTabOrder(self.Combo_Dinner, self.Combo_Bus)
        AddWorkWindow.setTabOrder(self.Combo_Bus, self.Edit_Reason)
        AddWorkWindow.setTabOrder(self.Edit_Reason, self.Btn_AddWork)
        AddWorkWindow.setTabOrder(self.Btn_AddWork, self.Edit_Status)

    def retranslateUi(self, AddWorkWindow):
        _translate = QtCore.QCoreApplication.translate
        AddWorkWindow.setWindowTitle(_translate("AddWorkWindow", "一键加班"))
        self.Label_User.setText(_translate("AddWorkWindow", "当前用户："))
        self.Label_CurUser.setText(_translate("AddWorkWindow", "哈哈哈哈哈"))
        self.Label_Dinner.setText(_translate("AddWorkWindow", "加班餐：  "))
        self.Label_Bus.setText(_translate("AddWorkWindow", "加班班车："))
        self.Label_Reason.setText(_translate("AddWorkWindow", "加班理由："))
        self.Combo_Dinner.setItemText(0, _translate("AddWorkWindow", "是"))
        self.Combo_Dinner.setItemText(1, _translate("AddWorkWindow", "否"))
        self.Combo_Bus.setItemText(0, _translate("AddWorkWindow", "是"))
        self.Combo_Bus.setItemText(1, _translate("AddWorkWindow", "否"))
        self.Btn_AddWork.setText(_translate("AddWorkWindow", "一键加班"))
        self.toolButton.setText(_translate("AddWorkWindow", "..."))

