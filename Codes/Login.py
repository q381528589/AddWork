# -*- coding: utf-8 -*-

import sys, logging
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
    #鼠标按下标志
    __m_flag = False
    #鼠标移动偏移
    __m_Position = 0
    
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
        try:
            file = open('./QT_UI/qss/Login.qss')
            styleSheet = file.readlines()
            styleSheet = ''.join(styleSheet).strip('\n')
            self.setStyleSheet(styleSheet)
        except IOError as err:
            logging.critical("无法加载QT_UI/qss/AddWork.qss：%s" % err)
        
        # 设置窗口标记（最小化|无边框|任务栏右键菜单）
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | 
                            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        
        #设置widget鼠标跟踪
        self.setMouseTracking(True)
        #设置鼠标跟踪判断默认值
        self.__InitDrag()

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
            

    #函数名称：CLogin::mousePressEvent
    #函数功能：触发鼠标按下事件
    #函数返回：无
    #函数参数：event    按键事件
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            #获取鼠标相对窗口的位置
            self.__m_Position = event.globalPos() - self.pos()
            #高于关闭按钮才有效
            if (self.__m_Position.y() <= self.Tool_Close.height()):
                self.__m_flag = True
                event.accept()
                #更改鼠标图标
                #self.setCursor(QtCore.Qt.OpenHandCursor)
    
    
    #函数名称：CLogin::mouseMoveEvent
    #函数功能：触发鼠标移动事件
    #函数返回：无
    #函数参数：QMouseEvent    鼠标事件        
    def mouseMoveEvent(self, QMouseEvent):
        if (QtCore.Qt.LeftButton and self.__m_flag):
            #更改窗口位置
            self.move(QMouseEvent.globalPos()-self.__m_Position)
            QMouseEvent.accept()
    
    
    #函数名称：CLogin::mouseReleaseEvent
    #函数功能：触发鼠标移出事件
    #函数返回：无
    #函数参数：QMouseEvent    鼠标事件          
    def mouseReleaseEvent(self, QMouseEvent):
        self.__m_flag = False
        #self.setCursor(QtCore.Qt.ArrowCursor)
    
                
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
    
    #函数名称：CLogin::initDrag
    #函数功能：#设置鼠标跟踪判断默认值
    #函数返回：无
    #函数参数：无 
    def __InitDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False    