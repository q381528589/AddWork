# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from RegisterUI import *

class CRegister(QtWidgets.QDialog, Ui_CRegister):
    _translate = QtCore.QCoreApplication.translate
    _cConfig = None
    #主窗口
    _cAddWork = None
    
    def __init__(self, cConfig):
        super(CRegister, self).__init__()
        self.setupUi(self)
        self.Combo_Dinner.setCurrentIndex(0)
        self.Combo_Bus.setCurrentIndex(1)
        self.Btn_Regist.clicked.connect(self.Regist)
        self._cConfig = cConfig

    def Show(self, cAddWork):
        self._cAddWork = cAddWork
        self.show()
        
    def Close(self):
        self.close()
            
    def Regist(self):
        self._cConfig.UserName = self.Text_User.text()
        if (None==self._cConfig.UserName or ""==self._cConfig.UserName):
            self.Label_Status.setText(self._translate("CRegister", "用户名不能为空"))
            return
        
        self._cConfig.Password = self.Text_Psw1.text()
        if (None==self._cConfig.Password or ""==self._cConfig.Password):
            self.Label_Status.setText(self._translate("CRegister", "密码不能为空"))
            return
        
        Password2 = self.Text_Psw2.text()
        if (None==Password2 or ""==Password2):
            self.Label_Status.setText(self._translate("CRegister", "密码不能为空"))
            return
        if (self._cConfig.Password != Password2):
            self.Label_Status.setText(self._translate("CRegister", "密码不一致"))
            return
        
        SrcRegCode = self.Text_RegCode.text()
        if (None==SrcRegCode or ""==SrcRegCode):
            self.Label_Status.setText(self._translate("CRegister", "注册码不能为空"))
            return
        if (False == self._CalcRegCode(SrcRegCode)):
            self.Label_Status.setText(self._translate("CRegister", "注册码不正确"))
            return
        
        szDinner = self.Combo_Dinner.currentText()
        if (None==szDinner or ""==szDinner):
            self.Label_Status.setText(self._translate("CRegister", "加班餐不能为空"))
            return
        if ("是" == szDinner):
            self._cConfig.Dinner = True
        elif ("否" == szDinner):
            self._cConfig.Dinner = False
        else:
            self.Label_Status.setText(self._translate("CRegister", "加班餐参数不正确"))
            return
        
        szBus = self.Combo_Bus.currentText()
        if (None==szBus or ""==szBus):
            self.Label_Status.setText(self._translate("CRegister", "加班班车不能为空"))
            return
        if ("是" == szBus):
            self._cConfig.Bus = True
        elif ("否" == szBus):
            self._cConfig.Bus = False
        else:
            self.Label_Status.setText(self._translate("CRegister", "加班班车参数不正确"))
            return
        
        self._cConfig.Reason = self.Text_Reason.text()
        
        #远程校验
        if (False == self._VerifyPsw()):
            return
        
        #写入文件
        self._cConfig.WriteFile()
        
        self.Label_Status.setText(self._translate("CRegister", "注册成功"))
        #跳转到主界面
        self.hide()
        self._cAddWork.Show(self._cConfig)
        
    def _CalcRegCode(self, SrcRegCode):
        RegCode = ""
        
        for i in range(0, len(SrcRegCode)):
            if ('-' != SrcRegCode[i]):
                RegCode += SrcRegCode[i]
               
        MD5Code = self._cConfig.CalcMD5(self._cConfig.UserName)
        MD5Code = MD5Code + "\0\0\0\0\0\0\0\0"
        MD5Code = self._cConfig.CalcMD5(MD5Code)
        
        RegCode = RegCode.upper()
        MD5Code = MD5Code.upper()
        if (RegCode != MD5Code[0:16]):
            return False
        
        return True
    
    #函数名称：CRegister::_VerifyPsw
    #函数功能：远程校验密码
    #函数返回：True成功 False失败
    #函数参数：无 
    def _VerifyPsw(self):
        nRet = self._cConfig.CheckUserPsw(self._cConfig.UserName, self._cConfig.Password)
        if (0 == nRet):
            return True
        elif (1 == nRet):
            self.Label_Status.setText(self._translate("CRegister", "填入的参数有误"))
            return False
        elif (2 ==nRet):
            self.Label_Status.setText(self._translate("CRegister", "网络错误"))
            return False
        elif (3 == nRet):
            self.Label_Status.setText(self._translate("CRegister", "用户名或密码错误"))
            return False
        
        return False