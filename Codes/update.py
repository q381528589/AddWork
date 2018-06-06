# -*- coding : utf-8 -*-

import os, sys, subprocess
import urllib.request
import threading
from PyQt5 import QtCore, QtWidgets
from updateUI import *

#下载路径
DOWNLOAD_PATH = "https://raw.githubusercontent.com/q381528589/Publisher/master/Addwork/"
APP_NAME = "AddWork.exe"

class CDownload(threading.Thread):
    Percent = 0
    bDownload = False
    
    def __init__(self):
        super(CDownload, self).__init__()
        
    def run(self):
        self.__HandleAddwork()
        return

    def Schedule(self, a,b,c):
        '''''
        a:已经下载的数据块
        b:数据块的大小
        c:远程文件的大小
       '''
        self.Percent = 100.0 * a * b / c
        if self.Percent > 100 :
            self.Percent = 100
        #print ('%.1f%%' % self.Percent)
        
    def __HandleAddwork(self):
        #获取网络上最新版本
        try:
            urllib.request.urlretrieve(DOWNLOAD_PATH+APP_NAME, 
                                       "./%s.download" % (APP_NAME), self.Schedule)
        except:
            print ("获取更新程序失败")
            return
        
        #关闭程序
        try:
            subprocess.check_call("taskkill /F /IM %s" % (APP_NAME))
        except:
            #TODO：用户手动关闭程序
            pass
        
        #下载更新完成
        self.bDownload = True
        return
    
class CUpdate(QtWidgets.QDialog, Ui_Dialog):
    __translate = QtCore.QCoreApplication.translate
    __cDownload = CDownload()
    __bShow = False
    
    def __init__(self):
        super(CUpdate, self).__init__()
        self.setupUi(self)
        self.Btn_OK.clicked.connect(self.__StartDownload)
    
    def closeEvent(self, event):
        #如果没有更新成功，在直接退出
        if (False == self.__cDownload.bDownload):
            event.accept()
            return
        
        #重命名文件
        if (os.path.exists("./%s" % (APP_NAME))):
            os.remove("./%s" % (APP_NAME))
        os.rename("./%s.download" % (APP_NAME), "./%s" % (APP_NAME))
        #写入版本文件
        self.__WriteLocalVersion()
        
        #关闭窗口
        event.accept()
        return
    
    def Update(self):
        #是否需要更新
        __bUpdate = False
        #update程序版本
        __UpdateVersion="0.0.0.0"
        #Addwork程序版本
        __AddWorkVersion="0.0.0.0"
        
        #获取自身版本号和其它版本号
        if (0 != self.__ReadLocalVersion()):
            #TODO：后期版本更新：文件不存在时校验MD5，两者均相同下载version.txt，否则执行后续更新步骤
            print ("读取本地文件发生错误")
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
                self.__WriteLocalVersion()
            #更新AddWork
            elif (-1 != VersionInfo.find("AddWork")):
                Version = VersionInfo.split('=')
                if (2 > len(Version)):
                    continue
                self.__bUpdate = self.__CheckVersion(self.__AddWorkVersion, Version[1])
                if (False == self.__bUpdate):
                    continue
                self.__UpdateAddwork(Version[1])
                #写入版本文件
                self.__AddWorkVersion = Version[1]
        
        #退出更新程序
        if (False == self.__bShow):
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
            return -1
        
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
        
        return 0
    
    def __WriteLocalVersion(self):
        szTemp = "update=%s\n" % (self.__UpdateVersion)
        szTemp += "AddWork=%s" % (self.__AddWorkVersion)
        try:
            File = open("./version.txt", 'w')
            File.write(szTemp)
            File.close()
        except IOError as err:
            print ("写入文件错误：%s" % (str(err)))
            
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
        elif (int(NewList[0]) < int(OldList[0])):
            return False
        
        if (int(NewList[1]) > int (OldList[1])):
            return True
        elif (int(NewList[1]) < int (OldList[1])):
            return False
        
        if (int(NewList[2]) > int (OldList[2])):
            return True
        elif (int(NewList[2]) < int (OldList[2])):
            return False
        
        #svn版本号更新的不算在列
        return False
                
    def __UpdateSelf(self):#TODO：多线程
        #静默更新
        #获取网络上最新版本
        try:
            f = urllib.request.urlopen(DOWNLOAD_PATH+"update.exe")
            data = f.read()
            f.close()
        except:
            print ("获取更新程序失败")
            sys.exit()
        #写至缓存文件
        try:
            File = open("./update.exe.download", "wb")
            File.write(data)
            File.close()
        except:
            print ("写入更新程序失败")
            sys.exit()
        #重命名文件
        if (os.path.exists("./update.exe.tmp")):
            os.remove("./update.exe.tmp")
        os.rename("./update.exe.download", "./update.exe.tmp")
        
        return
    
    def __UpdateProcessBar(self):
        while (True == self.__cDownload.isAlive()):  
            self.progressBar.setValue(self.__cDownload.Percent)  
            QtCore.QThread.msleep(100)
            QtWidgets.QApplication.processEvents()
        return
    
    def __UpdateAddwork(self, CurVersion):
        self.label.setText(self.__translate("Dialog", "发现新版本：%s，是否更新？") % (CurVersion))
        self.progressBar.hide()
        self.__bShow = True
        self.show()
        return
    
    def __StartDownload(self):
        self.label.hide()
        self.Btn_OK.setText(self.__translate("Dialog", "下载中……"))
        self.Btn_Cancel.setText(self.__translate("Dialog", "取消"))
        self.Btn_OK.setEnabled(False)
        self.progressBar.show()
        self.__cDownload.setDaemon(True)
        self.__cDownload.start()
        self.__UpdateProcessBar()
        self.Btn_OK.hide()
        self.Btn_Cancel.setText(self.__translate("Dialog", "完成"))
        return
              
if __name__ == "__main__":
    #加载QT窗口
    app = QtWidgets.QApplication(sys.argv)
    cUpdate = CUpdate()
    cUpdate.Update()
    sys.exit(app.exec_())