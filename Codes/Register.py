# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtGui import QCursor
from UI.RegisterUI import *

class CRegister(QtWidgets.QMainWindow, Ui_CRegister):
    _translate = QtCore.QCoreApplication.translate
    #配置文件
    _cConfig = None
    #Http
    _cHttp = None
    #窗口加载类
    _cLoadWindow = None
    #操作类
    _cOperation = None
    #鼠标按下标志
    __m_flag = False
    #鼠标移动偏移
    __m_Position = 0
    
    #函数名称：CRegister::__init__
    #函数功能：构造函数，用于构造注册窗口
    #函数返回：无
    #函数参数：cLoadWindow    所有窗口指针
    #函数参数：cConfig        用户基础配置
    #函数参数：cHttp          HTTP交互类
    def __init__(self, cLoadWindow, cConfig, cOperation):
        super(CRegister, self).__init__()
        self.setupUi(self)
        self.Combo_Dinner.setCurrentIndex(0)
        self.Combo_Bus.setCurrentIndex(1)
        self.Btn_Regist.clicked.connect(self.Regist)
        self._cConfig = cConfig
        self._cLoadWindow = cLoadWindow
        self._cOperation = cOperation
        
        self.Tool_Min.clicked.connect(self.showMinimized)
        self.Tool_Close.clicked.connect(self.close)
        
        #QSS界面美化设置
        file = open('./QT_UI/qss/Register.qss')
        styleSheet = file.readlines()
        styleSheet = ''.join(styleSheet).strip('\n')
        self.setStyleSheet(styleSheet)
        
        # 设置窗口标记（最小化|无边框|任务栏右键菜单）
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | 
                            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        
        #设置widget鼠标跟踪
        self.setMouseTracking(True)
        #设置鼠标跟踪判断默认值
        self.__InitDrag()
            
    #函数名称：CRegister::Show
    #函数功能：显示注册窗口
    #函数返回：无
    #函数参数：无
    def Show(self):
        self.show()
        
    #函数名称：CRegister::Close
    #函数功能：关闭注册窗口
    #函数返回：无
    #函数参数：无
    def Close(self):
        self.close()
        
    #函数名称：CRegister::keyPressEvent
    #函数功能：触发键盘事件
    #函数返回：无
    #函数参数：e    按键事件
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Enter:
            self.Regist()

    #函数名称：CRegister::mousePressEvent
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
    
    #函数名称：CRegister::mouseMoveEvent
    #函数功能：触发鼠标移动事件
    #函数返回：无
    #函数参数：QMouseEvent    鼠标事件        
    def mouseMoveEvent(self, QMouseEvent):
        if (QtCore.Qt.LeftButton and self.__m_flag):
            #更改窗口位置
            self.move(QMouseEvent.globalPos()-self.__m_Position)
            QMouseEvent.accept()
    
    #函数名称：CRegister::mouseReleaseEvent
    #函数功能：触发鼠标移出事件
    #函数返回：无
    #函数参数：QMouseEvent    鼠标事件          
    def mouseReleaseEvent(self, QMouseEvent):
        self.__m_flag = False
        #self.setCursor(QtCore.Qt.ArrowCursor)
        
    #函数名称：CRegister::Regist
    #函数功能：注册用户
    #函数返回：无
    #函数参数：无  
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
        
        self.Text_RegCode.setText(self._translate("CRegister", "开放注册阶段，目前无需注册码"))
        '''SrcRegCode = self.Text_RegCode.text()
        if (None==SrcRegCode or ""==SrcRegCode):
            self.Label_Status.setText(self._translate("CRegister", "注册码不能为空"))
            return
        if (False == self._CalcRegCode(SrcRegCode)):
            self.Label_Status.setText(self._translate("CRegister", "注册码不正确"))
            return'''
        
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
        self._cLoadWindow.ShowUI(2)
        self.hide()

    #函数名称：CRegister::Update
    #函数功能：更新程序
    #函数返回：无
    #函数参数：无          
    def Update(self):
        return

    #函数名称：CRegister::_CalcRegCode
    #函数功能：计算注册码的正确性
    #函数返回：True正确    False错误
    #函数参数：SrcRegCode    待验证的注册码
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
        nRet = self._cOperation.CheckUserPsw(self._cConfig.UserName, self._cConfig.Password)
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
    
    #函数名称：CRegister::initDrag
    #函数功能：#设置鼠标跟踪判断默认值
    #函数返回：无
    #函数参数：无 
    def __InitDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False