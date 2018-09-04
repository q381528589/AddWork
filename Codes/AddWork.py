# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, Qt

from UI.AddWorkUI import *
from Operation import COperation, CError
from Login import CLogin
from Register import CRegister
from HttpInteraction import CForm
from PyQt5.Qt import QMenu

#加班模块
class CAddWork(QtWidgets.QMainWindow, Ui_AddWorkWindow):
    _translate = QtCore.QCoreApplication.translate
    #确认加班
    _bCheck = False
    #用户配置
    _cConfig = None
    #窗口加载类
    _cLoadWindow = None
    #操作类
    _cOperation = None
    
    #函数名称：CAddWork::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：cLoadWindow    ：窗口加载类
    #函数参数：cConfig        ：用户配置
    #函数参数：cOpertation    ：http交互操作
    def __init__(self, cLoadWindow, cConfig, cOpertation):
        super(CAddWork, self).__init__()
        self.setupUi(self)
        #self.Btn_Exit.clicked.connect(self.Exit)
        self.Btn_AddWork.clicked.connect(self.AddWork)
        #self.Btn_ChgPsw.clicked.connect(self.ChangePsw)
        self.Tool_Min.clicked.connect(self.showMinimized)
        self.Tool_Close.clicked.connect(self.close)
        
        self._cConfig = cConfig
        self._cLoadWindow = cLoadWindow
        self._cOperation = cOpertation
            
        #检查用户是否已报名
        self.Btn_AddWork.setEnabled(False)
        self.Btn_AddWork.setText(self._translate("AddWorkWindow", "正在检查"))
        
        #设置下拉菜单
        menu = QMenu(self)
        self.ChgPsw = QtWidgets.QAction("修改密码", self)
        self.Logout = QtWidgets.QAction("退出登录", self)
        menu.addAction(self.ChgPsw)
        menu.addSeparator()
        menu.addAction(self.Logout)
        menu.addSeparator()
        self.Btn_Settings.setMenu(menu)
        self.ChgPsw.triggered.connect(self.ChangePsw)
        self.Logout.triggered.connect(self.Exit)
        
        #QSS界面美化设置
        file = open('./QT_UI/qss/AddWork.qss')
        styleSheet = file.readlines()
        styleSheet = ''.join(styleSheet).strip('\n')
        self.setStyleSheet(styleSheet)
        
        # 设置窗口标记（无边框|任务栏右键菜单）
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        
        #设置widget鼠标跟踪
        self.setMouseTracking(True)
        #设置鼠标跟踪判断默认值
        self.__InitDrag()

    #函数名称：CAddWork::Show
    #函数功能：显示加班窗口界面
    #函数返回：无
    #函数参数：无
    def Show(self):
        self._ReadConfig(self._cConfig)
        self.show()
    
    #函数名称：CAddWork::Show
    #函数功能：关闭加班窗口界面
    #函数返回：无
    #函数参数：无    
    def Close(self):
        self.close()
    
    #函数名称：CAddWork::Update
    #函数功能：执行更新操作
    #函数返回：无
    #函数参数：无    
    def Update(self):
        cError = CError()
        
        #构造加班检查类
        if (False == self._bCheck):
            #检查用户是否报名
            nRet = self._cOperation.CheckAddWork(self._cConfig)
            
            if (0 == nRet):
                self.Btn_AddWork.setEnabled(True)
                self.Btn_AddWork.setText(self._translate("AddWorkWindow", "一键加班"))
                self._bCheck = True
            elif (4 == nRet):
                self.Btn_AddWork.setEnabled(False)
                self.Btn_AddWork.setText(self._translate("AddWorkWindow", "已报名加班"))
                self._bCheck = True
            else:
                self._WriteStatus(cError.GetErrMsg(nRet))
                self.Btn_AddWork.setEnabled(True)
                self.Btn_AddWork.setText(self._translate("AddWorkWindow", "一键加班"))
                self._bCheck = True
         
        return
    
    #函数名称：CAddWork::_ReadConfig
    #函数功能：读取用户信息
    #函数返回：cConfig    ：用户信息配置
    #函数参数：无        
    def _ReadConfig(self, cConfig):
        #显示用户名
        self.Label_CurUser.setText(self._translate("AddWorkWindow", "%s" % (cConfig.UserName)))
        #加班餐
        Index = int(cConfig.Dinner)
        self.Combo_Dinner.setCurrentIndex((~Index)&0x01)
        #加班班车
        Index = int(cConfig.Bus)
        self.Combo_Bus.setCurrentIndex((~Index)&0x01)
        #加班理由
        self.Edit_Reason.setText(self._translate("AddWorkWindow", "%s" % (cConfig.Reason)))
    
    #函数名称：CAddWork::Exit
    #函数功能：退出登录
    #函数返回：无
    #函数参数：无        
    def Exit(self):
        #到登录界面
        self._cLoadWindow.CloseUI(3)
        self._cLoadWindow.ShowUI(1)
        self.hide()
    
    #函数名称：CAddWork::AddWork
    #函数功能：执行一键加班
    #函数返回：无
    #函数参数：无  
    def AddWork(self):
        #重新加班
        bReTry = False
        cForm = CForm()
        cError = CError()
        
        nRet = self._cOperation.AddWork(cForm, self._cConfig, bReTry)
        if (0 == nRet):
            #打印日志
            self._WriteStatus("\n一键加班脚本执行完成，请登录网页查看具体信息")
            self._WriteStatus("加班信息：")
            self._WriteStatus("加班时间：%s %s" % (cForm.data_91, cForm.data_67))
            self._WriteStatus("姓名：%s, 部门：%s, 加班餐：%s, 班车：%s, 加班理由：%s" % (cForm.data_68, cForm.data_70, cForm.data_89, cForm.data_90, cForm.data_73))
        elif (1==nRet or 2==nRet):
            #打印日志
            self._WriteStatus(cError.GetErrMsg(nRet))
            return
        elif (3 == nRet):
            self._WriteStatus(cError.GetErrMsg(nRet))
            return
        elif (5 == nRet):
            self._WriteStatus("新建表单失败，正在查找已有表单……")
            bReTry = True
        elif (6 == nRet):
            self._WriteStatus("获取表单信息发生错误，请重试")
            return
        else:
            self._WriteStatus("未知原因错误，请重试")
            return
        
        #重新加班
        if (True == bReTry):
            nRet = self._cOperation.AddWork(cForm, self._cConfig, bReTry)
            if (0 == nRet):
                #打印日志
                self._WriteStatus("\n一键加班脚本执行完成，请登录网页查看具体信息")
                self._WriteStatus("加班信息：")
                self._WriteStatus("加班时间：%s %s" % (cForm.data_91, cForm.data_67))
                self._WriteStatus("姓名：%s, 部门：%s, 加班餐：%s, 班车：%s, 加班理由：%s" % (cForm.data_68, cForm.data_70, cForm.data_89, cForm.data_90, cForm.data_73))
            elif (1==nRet or 2==nRet):
                #打印日志
                self._WriteStatus(cError.GetErrMsg(nRet))
                return
            elif (3 == nRet):
                self._WriteStatus(cError.GetErrMsg(nRet))
                return
            elif (6 == nRet):
                self._WriteStatus("获取表单信息发生错误，请重试")
                return
            else:
                self._WriteStatus("未知原因错误，请重试")
                return
        
        #设置一键加班为disable
        self.Btn_AddWork.setEnabled(False)
        self.Btn_AddWork.setText(self._translate("AddWorkWindow", "已报名加班"))
        
        #更新文件
        if (True == self._cConfig.bUpdate):
            self._cConfig.WriteFile()
        return
    
    #函数名称：CAddWork::ChangePsw
    #函数功能：弹出修改密码界面
    #函数返回：无
    #函数参数：无  
    def ChangePsw(self):
        #到修改密码界面
        self._cLoadWindow.ShowUI(3)
        

    #函数名称：CAddWork::eventFilter
    #函数功能：处理事件操作
    #函数返回：False无任何操作（不要返回True，否则会触发异常事件）
    #函数参数：obj      ：目标模块
    #函数参数：event    ：触发事件
    def eventFilter(self, obj, event):
        #只处理失去焦点的事件
        if (event.type() != QtCore.QEvent.FocusOut):
            return False
        
        #加班理由修改
        if (obj==self.Edit_Reason \
                and self._cConfig.Reason!=self.Edit_Reason.text()):
            self._cConfig.Reason = self.Edit_Reason.text()
            if (0 != self._cConfig.WriteFile()):
                self._WriteStatus("修改加班字段失败：详情见日志")
        
        #加班餐修改
        if (obj==self.Combo_Dinner):
            Index = self.Combo_Dinner.currentIndex()
            if (self._cConfig.Dinner == (~Index)&0x01):
                return False
            self._cConfig.Dinner = (~Index)&0x01
            if (0 != self._cConfig.WriteFile()):
                self._WriteStatus("修改加班餐字段失败：详情见日志")
                
        #加班班车修改
        if (obj==self.Combo_Bus):
            Index = self.Combo_Bus.currentIndex()
            if (self._cConfig.Bus == (~Index)&0x01):
                return False
            self._cConfig.Bus = (~Index)&0x01
            if (0 != self._cConfig.WriteFile()):
                self._WriteStatus("修改加班班车字段失败：详情见日志")
                       
        #更新文件
        if (True == self._cConfig.bUpdate):
            self._cConfig.WriteFile()
        return False
    
    #函数名称：CAddWork::mousePressEvent
    #函数功能：触发鼠标按下事件
    #函数返回：无
    #函数参数：event    按键事件
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            self.__m_flag = True
            #获取鼠标相对窗口的位置
            self.__m_Position = event.globalPos() - self.pos()
            event.accept()
            #更改鼠标图标
            self.setCursor(QtCore.Qt.OpenHandCursor)
    
    #函数名称：CAddWork::mouseMoveEvent
    #函数功能：触发鼠标移动事件
    #函数返回：无
    #函数参数：QMouseEvent    鼠标事件        
    def mouseMoveEvent(self, QMouseEvent):
        if (QtCore.Qt.LeftButton and self.__m_flag):
            #更改窗口位置
            self.move(QMouseEvent.globalPos()-self.__m_Position)
            QMouseEvent.accept()
    
    #函数名称：CAddWork::mouseReleaseEvent
    #函数功能：触发鼠标移出事件
    #函数返回：无
    #函数参数：QMouseEvent    鼠标事件          
    def mouseReleaseEvent(self, QMouseEvent):
        self.__m_flag = False
        self.setCursor(QtCore.Qt.ArrowCursor)
    
    #函数名称：CAddWork::_WriteStatus
    #函数功能：在界面打印状态信息
    #函数返回：无
    #函数参数：szData   ：要打印的信息
    def _WriteStatus(self, szData):
        self.Edit_Status.appendPlainText(szData)
        QtWidgets.QApplication.processEvents()
    
    #函数名称：CAddWork::initDrag
    #函数功能：#设置鼠标跟踪判断默认值
    #函数返回：无
    #函数参数：无 
    def __InitDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False  