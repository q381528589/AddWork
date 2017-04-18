# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from LoginUI import *

#登录窗口
class CLogin(QtWidgets.QMainWindow, Ui_LoginWindow):
    _translate = QtCore.QCoreApplication.translate
    #配置文件
    _cConfig = None
    
    #主窗口
    _cAddWork = None

    #函数名称：CLogin::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：cConfig    ：配置文件
    def __init__(self, cConfig):
        super(CLogin, self).__init__()
        self.setupUi(self)
        self.Btn_Login.clicked.connect(self.Login)
        
        self._cConfig = cConfig
        self.Label_ShowUser.setText(self._translate("LoginWindow", cConfig.UserName))


    #函数名称：CLogin::Show
    #函数功能：显示窗口
    #函数返回：无
    #函数参数：cAddWork    ：用于回传显示的主窗口界面
    def Show(self, cAddWork, cConfig):
        self._cAddWork = cAddWork
        self.Label_ShowUser.setText(self._translate("LoginWindow", cConfig.UserName))
        if (True == cConfig.bSkip):
            self.Check_NoPsw.toggle()
        self.show()


    #函数名称：CLogin::Close
    #函数功能：关闭窗口
    #函数返回：无
    #函数参数：无     
    def Close(self):
        self.close()


    #函数名称：CLogin::Login
    #函数功能：登录，成功后切到主窗口
    #函数返回：无
    #函数参数：无                
    def Login(self):
        if (None == self._cAddWork):
            raise ValueError("系统错误：主窗口未被传值至登录窗口")
            
        Password = self.Text_Psw.text()
        if (None==Password or ""==Password):
            self.Label_Status.setText(self._translate("LoginWindow", "密码不能为空"))
            return
        
        #验证密码
        if (self._cConfig.Password != Password):
            #远程校验
            self.Label_Status.setText(self._translate("LoginWindow", "正在与服务器校验密码……"))
            if (False == self._VerifyPsw(Password)):
                return
            #远程校验成功,更新本地数据
            self._cConfig.Password = Password
            self.Label_Status.setText(self._translate("LoginWindow", "正在更新密码……"))
            self._cConfig.WriteFile()
            self._cAddWork.Show(self._cConfig)
            
        #清除显示的密码
        self.Text_Psw.setText(self._translate("LoginWindow", ""))

        #根据复选框结果决定是否重写配置文件
        if (self.Check_NoPsw.isChecked()):
            self._cConfig.bSkip = True
            self._cConfig.WriteFile()
                    
        #跳转至主界面
        self.hide()
        self._cAddWork.Show(self._cConfig)

    #函数名称：CLogin::_VerifyPsw
    #函数功能：远程校验密码
    #函数返回：True成功 False失败
    #函数参数：Password    :需要验证的密码
    def _VerifyPsw(self, Password):
        nRet = self._cConfig.CheckUserPsw(self._cConfig.UserName, Password)
        if (0 == nRet):
            return True
        elif (1 == nRet):
            self.Label_Status.setText(self._translate("LoginWindow", "填入的参数有误"))
            return False
        elif (2 ==nRet):
            self.Label_Status.setText(self._translate("LoginWindow", "网络错误"))
            return False
        elif (3 == nRet):
            self.Label_Status.setText(self._translate("LoginWindow", "用户名或密码错误"))
            return False
        
        return False
        