# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from AddWork import *
from ConfigFileIO import CFileMng, CConfig
from DESCode import CDESCode
import logging

Version = "2.0.0"
    
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
                        filemode='w+')
    #读取配置文件
    if (0 == cConfig.ReadFile()):
        bReadFile = True
    
    #加载QT登录主窗口
    app = QtWidgets.QApplication(sys.argv)
    cAddWork = CAddWork(cConfig, bReadFile)
    sys.exit(app.exec_())
