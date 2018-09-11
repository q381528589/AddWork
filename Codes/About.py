# -*- coding: utf-8 -*-

import logging
from UI.AboutUI import *
from ConfigFileIO import CFileMng

#关于模块
class CAbout(QtWidgets.QDialog, Ui_About):
    _translate = QtCore.QCoreApplication.translate
    #鼠标按下标志
    __m_flag = False
    #鼠标移动偏移
    __m_Position = 0
    
    #函数名称：CAbout::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：cLoadWindow    ：窗口加载类
    #函数参数：cConfig        ：用户配置
    #函数参数：cOpertation    ：http交互操作
    def __init__(self, cLoadWindow, cConfig, cOpertation):
        super(CAbout, self).__init__()
        self.setupUi(self)
        self.Label_Version.setText(self._translate("About", "软件版本: %s") % cConfig.Version)
        self.Tool_Close.clicked.connect(self.close)
        
        #QSS界面美化设置
        try:
            file = open('./QT_UI/qss/About.qss')
            styleSheet = file.readlines()
            styleSheet = ''.join(styleSheet).strip('\n')
            self.setStyleSheet(styleSheet)
        except IOError as err:
            logging.critical("无法加载QT_UI/qss/About.qss：%s" % err)
        
        #设置窗口标记（无边框|无任务栏|窗口最前）
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | 
                            QtCore.Qt.SplashScreen| QtCore.Qt.WindowStaysOnTopHint)
        
        #设置widget鼠标跟踪
        self.setMouseTracking(True)
        #设置鼠标跟踪判断默认值
        self.__InitDrag()
        
    #函数名称：CAbout::Show
    #函数功能：显示关于窗口界面
    #函数返回：无
    #函数参数：无
    def Show(self):
        self.show()
        
    #函数名称：CAbout::Close
    #函数功能：关闭关于窗口界面
    #函数返回：无
    #函数参数：无    
    def Close(self):
        self.close()
        
    #函数名称：CAbout::Update
    #函数功能：执行更新操作
    #函数返回：无
    #函数参数：无    
    def Update(self):
        pass
    
    #函数名称：CAbout::mousePressEvent
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
    
    #函数名称：CAbout::mouseMoveEvent
    #函数功能：触发鼠标移动事件
    #函数返回：无
    #函数参数：QMouseEvent    鼠标事件        
    def mouseMoveEvent(self, QMouseEvent):
        if (QtCore.Qt.LeftButton and self.__m_flag):
            #更改窗口位置
            self.move(QMouseEvent.globalPos()-self.__m_Position)
            QMouseEvent.accept()
    
    #函数名称：CAbout::mouseReleaseEvent
    #函数功能：触发鼠标移出事件
    #函数返回：无
    #函数参数：QMouseEvent    鼠标事件          
    def mouseReleaseEvent(self, QMouseEvent):
        self.__m_flag = False
        #self.setCursor(QtCore.Qt.ArrowCursor)
    
    #函数名称：CAbout::initDrag
    #函数功能：#设置鼠标跟踪判断默认值
    #函数返回：无
    #函数参数：无 
    def __InitDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False  