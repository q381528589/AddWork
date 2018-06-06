# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from UI.ChgPswUI import *
from Operation import CError

#修改密码窗口
class CChgPsw(QtWidgets.QMainWindow, Ui_ChgPswWindow):
    _translate = QtCore.QCoreApplication.translate
    #配置文件
    _cConfig = None
    #窗口加载类
    _cLoadWindow = None
    #操作类
    _cOperation = None
    
    #函数名称：CChgPsw::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：cLoadWindow：加载窗口类
    #函数参数：cConfig    ：配置文件
    #函数参数：cHttp      ：HTTP交互类
    def __init__(self, cLoadWindow, cConfig, cOpertation):
        super(CChgPsw, self).__init__()
        self.setupUi(self)
        self.Btn_OK.clicked.connect(self.__ChangePsw)
        self.Btn_Clear.clicked.connect(self.__ClearPsw)
        self._cConfig = cConfig
        self._cLoadWindow = cLoadWindow
        self._cOperation = cOpertation
        
    #函数名称：CChgPsw::Show
    #函数功能：显示窗口
    #函数返回：无
    def Show(self):
        self.show()

    #函数名称：CChgPsw::Close
    #函数功能：关闭窗口
    #函数返回：无
    #函数参数：无     
    def Close(self):
        self.close()
        
    #函数名称：CChgPsw::Update
    #函数功能：更新程序
    #函数返回：无
    #函数参数：无
    def Update(self):
        return
    
    #函数名称：CChgPsw::__ChangePsw
    #函数功能：修改密码
    #函数返回：无
    #函数参数：无
    def __ChangePsw(self):
        cError = CError()
        OldPsw = self.Text_OldPsw.text()
        NewPsw = self.Text_NewPsw.text()
        CheckPsw = self.Text_CheckPsw.text()
        
        #检查新密码
        if (len(NewPsw)<8 or len(NewPsw)>20):
            QMessageBox.information(self, "提示", self.tr("新密码长度要求8-20位，并包含字母和数字"))
            return
        #检查确认新密码
        if (NewPsw != CheckPsw):
            QMessageBox.information(self, "提示", self.tr("第二次密码与第一次密码不一致"))
            return
        
        nRet = self._cOperation.ChangePsw(self._cConfig, OldPsw, NewPsw, cError)
        if (0 != nRet):
            QMessageBox.information(self, "提示", self.tr("%s" % (cError.GetErrMsg(nRet))))
            return
        else:
            QMessageBox.information(self, "提示", self.tr("密码修改成功"))
            self.Close()
            return
        
        #修改本地用户配置
        self._cConfig.Password = NewPsw
        self._cConfig.bFileChange = True
        self._cConfig.WriteFile()
        return
    
    #函数名称：CChgPsw::__ClearPsw
    #函数功能：重置对话框
    #函数返回：无
    #函数参数：无
    def __ClearPsw(self):    
        self.Text_OldPsw.setText(self._translate("ChgPswWindow", ""))
        self.Text_NewPsw.setText(self._translate("ChgPswWindow", ""))
        self.Text_CheckPsw.setText(self._translate("ChgPswWindow", ""))
        return