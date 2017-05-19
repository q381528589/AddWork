# -*- coding : utf-8 -*-

import os, sys, subprocess
import urllib
from PyQt5 import QtWidgets
from updateUI import *

#下载路径
DOWNLOAD_PATH = "https://raw.githubusercontent.com/q381528589/Publisher/master/Addwork/"

class CUpdate(QtWidgets.QMainWindow, Ui_UpdateWindow):
    __translate = QtCore.QCoreApplication.translate
    
    def __init__(self):
        super(CUpdate, self).__init__()
        self.setupUi(self)
        self.__Init()
    
    def __Init(self):
        #是否需要更新
        __bUpdate = False
        #update程序版本
        __UpdateVersion=""
        #Addwork程序版本
        __AddWorkVersion=""
        
        #获取自身版本号和其它版本号
        self.__ReadLocalVersion()
        if (""==self.__UpdateVersion or ""==self.__AddWorkVersion):
            sys.exit()
        #获取网络上最新版本号
        try:
            f = urllib.request.urlopen(DOWNLOAD_PATH+"version.txt")
            data = f.read().decode("utf-8")
            f.close()
        except:
            print ("获取版本信息失败")
            sys.exit()
        VersionList = data.split("\r\n")
        for VersionInfo in VersionList:
            #更新update
            if (-1 != VersionInfo.find("update")):
                Version = VersionInfo.split('=')
                if (2 > len(Version)):
                    continue
                self.__bUpdate = self.__CheckVersion(self.__UpdateVersion, Version[1])
                if (False == self.__bUpdate):
                    continue
                self.__UpdateSelf()
                #写入版本文件
                self.__UpdateVersion = Version[1]
            #更新AddWork
            elif (-1 != VersionInfo.find("AddWork")):
                Version = VersionInfo.split('=')
                if (2 > len(Version)):
                    continue
                self.__bUpdate = self.__CheckVersion(self.__AddWorkVersion, Version[1])
                if (False == self.__bUpdate):
                    continue
                self.__UpdateAddwork()
                #写入版本文件
                self.__AddWorkVersion = Version[1]
        
        #TODO：更新版本文件
        #self.WriteLocalVersion()
        #退出更新程序
        sys.exit()
        return
    
    def __ReadLocalVersion(self):
        try:
            File = open("./version.txt", 'r')
            Text = File.read()
            List = Text.split("\n")
            File.close()
        except:
            print ("打开文件错误")
            sys.exit()
        
        for VersionInfo in List:
            #update版本
            if (-1 != VersionInfo.find("update")):
                Version = VersionInfo.split('=')
                if (2 > len(Version)):
                    continue
                self.__UpdateVersion = Version[1]
            #AddWork版本
            elif (-1 != VersionInfo.find("AddWork")):
                Version = VersionInfo.split('=')
                if (2 > len(Version)):
                    continue
                self.__AddWorkVersion = Version[1]
        
        return
                
    def __CheckVersion(self, OldVersion, NewVersion):
        OldList = OldVersion.split('.')
        NewList = NewVersion.split('.')
        
        if (4!=len(NewList) or 4!=len(OldList)):
            return False
        
        #检查版本
        if (int(NewList[0]) > int(OldList[0])):
            #大版本更新
            return True
        elif (int(NewList[1]) > int (OldList[1])):
            return True
        elif (int(NewList[2]) > int (OldList[2])):
            return True
        
        #svn版本号更新的不算在列
        return False
                
    def __UpdateSelf(self):
        #静默更新
        #获取网络上最新版本
        try:
            f = urllib.request.urlopen(DOWNLOAD_PATH+"update.exe")
            data = f.read()
            f.close()
        except:
            print ("获取更新程序失败")
            return
        #写至缓存文件
        try:
            File = open("./update.exe.download", "wb")
            File.write(data)
            File.close()
        except:
            print ("写入更新程序失败")
        #重命名文件
        os.rename("./update.exe.download", "./update.exe.tmp")
    
    def __UpdateAddwork(self):
        #先提示用户是否更新
        button=QtWidgets.QMessageBox.question(self,"Question",  
                                    self.tr("检测到最新版本，是否更新？"),  
                                    QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel,  
                                    QtWidgets.QMessageBox.Ok)  
        if (button==QtWidgets.QMessageBox.Ok):
            self.show()
            self.__HandleAddwork()
        elif (button==QtWidgets.QMessageBox.Cancel):  
            return
        else:  
            return
    
    def __HandleAddwork(self):
        #获取网络上最新版本
        try:
            f = urllib.request.urlopen(DOWNLOAD_PATH+"AddWork.exe")
            data = f.read()
            f.close()
        except:
            print ("获取更新程序失败")
            return
        
        #关闭程序
        Status = subprocess.check_call("taskkill /F /IM AddWork.exe")
        if (0 != Status):
            #TODO：用户手动关闭程序
            pass
        
        #写至缓存文件
        try:
            File = open("./AddWork.exe.download", "wb")
            File.write(data)
            File.close()
        except:
            print ("写入更新程序失败")
        #重命名文件
        
        os.rename("./update.exe.download", "./update.exe.tmp")
        #TODO：提示
        
if __name__ == "__main__":
    #加载QT窗口
    app = QtWidgets.QApplication(sys.argv)
    cUpdate = CUpdate()
    sys.exit(app.exec_())