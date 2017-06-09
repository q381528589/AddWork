# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from AddWork import *
from ConfigFileIO import CFileMng, CConfig
from DESCode import CDESCode
import os, logging

class CUpdateApp:
    def __init__(self):
        pass
    
    def StartUpdate(self):
        #覆盖更新
        if (os.path.exists("./update.exe.tmp")):
            #移除旧版update程序
            if (os.path.exists("./update.exe")):
                os.remove("./update.exe")
            #重命名
            os.rename("./update.exe.tmp", "./update.exe")
            
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
    cAddWork = CAddWork(cConfig, bReadFile)
    sys.exit(app.exec_())
