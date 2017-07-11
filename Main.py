# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from Register import *
from Login import *
from AddWork import *
from ConfigFileIO import CFileMng, CConfig
from DESCode import CDESCode
import os, logging

#启动自动更新程序
class CUpdateApp:
    #函数名称：CUpdateApp::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        pass
    
    #函数名称：CUpdateApp::StartUpdate
    #函数功能：启动自动更新程序
    #函数返回：无
    #函数参数：无
    def StartUpdate(self):
        #覆盖更新
        if (os.path.exists("./update.exe.tmp")):
            #移除旧版update程序
            if (os.path.exists("./update.exe")):
                os.remove("./update.exe")
            #重命名
            os.rename("./update.exe.tmp", "./update.exe")
        
        #检查程序是否存在
        if (False == os.path.exists("./update.exe")):
            logging.critical("执行更新程序失败:更新程序不存在")
            return 
          
        #启动程序
        try:
            import subprocess
            from subprocess import Popen, PIPE
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            p = Popen([r'update.exe'], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=os.getcwd(), startupinfo=si)
        except:
            logging.critical("执行更新程序失败")
            return
        
        return

#主程序，用于加载窗口
class CMain:
    #用户配置
    m_cConfig = None
    #注册界面
    m_pcRegister = None
    #登录界面
    m_pcLogin = None
    #加班界面
    m_pcAddWork = None
    #修改密码界面
    m_pcChangePsw = None
    
    #函数名称：CMain::__init__
    #函数功能：构造函数，根据初始配置决定加载哪个界面
    #函数返回：无
    #函数参数：bReadFile    是否有配置文件
    #函数参数：cConfig      用户基础配置
    def __init__(self, bReadFile, cConfig):
        self.m_cConfig = cConfig
        #注册界面
        if (False == bReadFile):
            self.m_pcRegister = CRegister(self, cConfig)
            self.m_pcRegister.Show()
        #登录界面
        elif (False == cConfig.bSkip):
            self.m_pcLogin = CLogin(self, cConfig)
            self.m_pcLogin.Show()
        #加班界面
        else:
            self.m_pcAddWork = CAddWork(self, cConfig)
            self.m_pcAddWork.Show()
    
    #函数名称：CMain::ShowUI
    #函数功能：显示UI界面
    #函数返回：无
    #函数参数：UIIndex    对应的界面框，0注册；1登录；2加班；3修改密码
    def ShowUI(self, UIIndex):
        if (0 == UIIndex):
            if (None == self.m_pcRegister):
                self.m_pcRegister = CRegister(self, self.m_cConfig)
            self.m_pcRegister.Show()
        elif (1 == UIIndex):
            if (None == self.m_pcLogin):
                self.m_pcLogin = CLogin(self, self.m_cConfig)
            self.m_pcLogin.Show()
        elif (2 == UIIndex):
            if (None == self.m_pcAddWork):
                self.m_pcAddWork = CAddWork(self, self.m_cConfig)
            self.m_pcAddWork.Show()
        else:
            logging.error("没有找到有效的窗口界面")
            return -1
        
        return 0
        
if __name__ == '__main__':
    #加解密算法
    cDesCode = CDESCode()
    #配置文件
    cCfgFile = CFileMng("./AddWork.cfg")
    #用户配置
    cConfig = CConfig(cCfgFile, cDesCode)
    #读取配置是否成功
    bReadFile = False
    
    #加载日志模块
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='AddWork.log',
                        filemode='a+')
    #读取配置文件
    if (0 == cConfig.ReadFile()):
        bReadFile = True
    
    #启动update
    cApp = CUpdateApp()
    cApp.StartUpdate()
    
    #加载QT登录主窗口
    app = QtWidgets.QApplication(sys.argv)
    cMain = CMain(bReadFile, cConfig)
    sys.exit(app.exec_())