# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from UI.LoginUI import *

#登录窗口
class CLogin(QtWidgets.QMainWindow, Ui_LoginWindow):
    _translate = QtCore.QCoreApplication.translate
    #配置文件
    _cConfig = None
    #窗口加载类
    _cLoadWindow = None
    #操作类
    _cOperation = None

    #函数名称：CLogin::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：cLoadWindow：加载窗口类
    #函数参数：cConfig    ：配置文件
    #函数参数：cHttp      ：HTTP交互类
    def __init__(self, cLoadWindow, cConfig, cOpertation):
        super(CLogin, self).__init__()
        self.setupUi(self)
        self.Btn_Login.clicked.connect(self.Login)
        self._cConfig = cConfig
        self._cLoadWindow = cLoadWindow
        self._cOperation = cOpertation
        self.Label_ShowUser.setText(self._translate("LoginWindow", cConfig.UserName))
        
        #设置最小化和关闭
        self.Tool_Min.clicked.connect(self.showMinimized)
        self.Tool_Close.clicked.connect(self.close)
        
        #加载QSS
        file = open('./QT_UI/qss/Login.qss')
        styleSheet = file.readlines()
        styleSheet = ''.join(styleSheet).strip('\n')
        self.setStyleSheet(styleSheet)
        
        # 设置窗口标记（无边框|任务栏右键菜单）
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)

    #函数名称：CLogin::Show
    #函数功能：显示窗口
    #函数返回：无
    def Show(self):
        self.Label_ShowUser.setText(self._translate("LoginWindow", self._cConfig.UserName))
        if (True == self._cConfig.bSkip):
            #下次不需要登录（勾选选项框）
            self.Check_NoPsw.toggle()
        self.show()


    #函数名称：CLogin::Close
    #函数功能：关闭窗口
    #函数返回：无
    #函数参数：无     
    def Close(self):
        self.close()


    #函数名称：CLogin::keyPressEvent
    #函数功能：触发键盘事件
    #函数返回：无
    #函数参数：e        ：键盘事件
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Enter:
            self.Login()
            
            
    #函数名称：CLogin::Login
    #函数功能：登录，成功后切到主窗口
    #函数返回：无
    #函数参数：无                
    def Login(self):
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
            
        #清除显示的密码
        self.Text_Psw.setText(self._translate("LoginWindow", ""))

        #复选框结果
        if (self.Check_NoPsw.isChecked()):
            self._cConfig.bSkip = True
        else:
            self._cConfig.bSkip = False
        
        #新配置写入文件
        self._cConfig.WriteFile()
                    
        #跳转至主界面
        self._cLoadWindow.ShowUI(2)
        self.hide()

    #函数名称：CLogin::Update
    #函数功能：更新程序
    #函数返回：无
    #函数参数：无
    def Update(self):
        return 
    
    #函数名称：CLogin::_VerifyPsw
    #函数功能：远程校验密码
    #函数返回：True成功 False失败
    #函数参数：Password    :需要验证的密码
    def _VerifyPsw(self, Password):
        nRet = self._cOperation.CheckUserPsw(self._cConfig.UserName, Password)
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
        