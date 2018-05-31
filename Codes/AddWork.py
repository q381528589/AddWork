# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from UI.AddWorkUI import *
from Login import CLogin
from Register import CRegister
import base64, urllib, urllib.request, time
from HttpInteraction import CHttp, CForm, CRegex, CMIME

#检查是否加班
class CCheckAddWork:
    #用户配置
    __cConfig = None
    #是否已加班
    bAddWork = False
    
    def __init__(self, cConfig):
        self.__cConfig = cConfig
    
    def Check(self):
        cHttp = CHttp()
        cRegex = CRegex()
        #登录成功定义
        SuccessStr = "正在进入OA系统，请稍候..."
        
        #检测数据有效性
        if (None==self.__cConfig.UserName or None==self.__cConfig.Password or \
                0==len(self.__cConfig.Reason)):
            return
        
        #维持长链
        cHttp.SetReqHead("Connection", "Keep-Alive")
    
        #Step1：连接
        cHttp.Connect()
    
        #Step2：登录
        if (False == cHttp.ValidCookie()):
            nRet = self.__cConfig.CheckUserPsw(self.__cConfig.UserName, self.__cConfig.Password)
            if (0 != nRet):
                cHttp.Close()
                return
        
        #Step3:查询记录
        #组装日期
        cTime = time.localtime()
        Date = "%s年" % (cTime.tm_year)
        Date += str(cTime.tm_mon) if (cTime.tm_mon>=10) else ("0"+str(cTime.tm_mon))
        Date += "月"
        Date += str(cTime.tm_mday) if (cTime.tm_mday>=10) else ("0"+str(cTime.tm_mday))
        Date += "日"
        Date = urllib.request.quote(Date.encode("utf-8"))
        ReqUrl = "/general/workflow/list/data/getdata.php?pageType=settles&searchType=adv&flow_id=131&run_name=%s" % (Date)
        ReqBody = "_search=false&nd=%ld&rows=10&page=1&sidx=run_id&sord=desc" % (time.time()*1000)
        if (False == cHttp.Send("POST", ReqUrl)):
            cHttp.Close()
            return
        AckCode, AckHead, AckBody = cHttp.Receive()
        if (200 != AckCode):
            cHttp.Close()
            return
        
        szRegexTemp = r"\{[\s]*\"records\"\:[\s]*\"([\d]+)\","
        Result = cRegex.Match(szRegexTemp, AckBody.decode("GBK"), 1)
        if (None == Result):
            cHttp.Close()
            return
        #已报名加班
        if ('0' != Result):
            self.bAddWork = True
        
        #Step4：关闭连接
        cHttp.Close()
        
        return
    
    
class CAddWork(QtWidgets.QMainWindow, Ui_AddWorkWindow):
    _translate = QtCore.QCoreApplication.translate
    _cConfig = None
    #确认加班
    _cCheck = None
    #窗口加载类
    _cLoadWindow = None
    
    def __init__(self, cLoadWindow, cConfig):
        super(CAddWork, self).__init__()
        self.setupUi(self)
        self.Btn_Exit.clicked.connect(self.Exit)
        self.Btn_AddWork.clicked.connect(self.AddWork)
        self.Btn_ChgPsw.clicked.connect(self.ChangePsw)
        
        self._cConfig = cConfig
        self._cLoadWindow = cLoadWindow
            
        #检查用户是否已报名
        self.Btn_AddWork.setEnabled(False)
        self.Btn_AddWork.setText(self._translate("AddWorkWindow", "正在检查"))
        
    
    def Show(self):
        self._ReadConfig(self._cConfig)
        self.show()
        
    def Close(self):
        self.close()
    
    def Update(self):
        #构造加班检查类
        if (None == self._cCheck):
            #检查用户是否报名
            self._cCheck = CCheckAddWork(self._cConfig)
            self._cCheck.Check()
            if (True == self._cCheck.bAddWork):
                self.Btn_AddWork.setEnabled(False)
                self.Btn_AddWork.setText(self._translate("AddWorkWindow", "已报名加班"))
            else:
                self.Btn_AddWork.setEnabled(True)
                self.Btn_AddWork.setText(self._translate("AddWorkWindow", "一键加班"))
                
        return
        
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
        
    def Exit(self):
        #到登录界面
        self._cLoadWindow.ShowUI(1)
        self.hide()
    
    def AddWork(self):
        cHttp = CHttp()
        cForm = CForm()
        cRegex = CRegex()
        cMime = CMIME()
        #登录成功定义
        SuccessStr = "正在进入OA系统，请稍候..."
        #登录失败日志
        LogErrMsg = ["登录成功", "参数错误", "网络错误", "用户名或密码错误"]
        
        #检测数据有效性
        if (None==self._cConfig.UserName or None==self._cConfig.Password or \
                0==len(self._cConfig.Reason)):
            return
        #维持长链
        cHttp.SetReqHead("Connection", "Keep-Alive")
    
        #Step1：连接
        cHttp.Connect()
    
        #Step2：登录
        if (False == cHttp.ValidCookie()):
            nRet = self.__cConfig.CheckUserPsw(self.__cConfig.UserName, self.__cConfig.Password)
            if (0 != nRet):
                self._WriteStatus(LogErrMsg[nRet])
    
        #Step3：提取表单
        cHttp.DelReqHead("Origin")
        cHttp.DelReqHead("Content-Type")
        if (False == cHttp.Send("GET", "/general/workflow/new/edit.php?FLOW_ID=%s&AUTO_NEW=1" % cForm.flow_id)):
            self._WriteStatus("发送HTTP请求失败")
            cHttp.Close()
            return
        AckCode, AckHead, AckBody = cHttp.Receive()
        #验证表单数据
        pszUrlTemp = None
        if (302 == AckCode):
            for HeadType in AckHead:
                if (HeadType[0] == "location"):
                    pszUrlTemp = HeadType[1]
        elif (200 == AckCode):
            self._WriteStatus("新建表单失败，正在查找已有表单数据……")
            #请求数据
            ReqUrl = "/portal/personal/workflow.php"
            if (False == cHttp.Send("GET", ReqUrl)):
                self._WriteStatus("发送HTTP请求失败")
                cHttp.Close()
                return
            AckCode, AckHead, AckBody = cHttp.Receive()
            if (200 != AckCode):
                self._WriteStatus("HTTP错误：%d" % (AckCode))
                cHttp.Close()
                return
            #获取当前系统时间
            cTime = time.localtime()
            #查找表单数据。构建正则表达式
            szRegexTemp = "<td align=\"left\">.*?openURL\(.*?,.*?,'(.*?)'\)\">加班登记"
            szRegexTemp += "（%s年[0]?%s月[0]?%s日）" % (str(cTime.tm_year), str(cTime.tm_mon), str(cTime.tm_mday))
            szRegexTemp += ".*?-%s" % self._cConfig.UserName
            pszUrlTemp = cRegex.Match(szRegexTemp, AckBody, 1)
            if (None == pszUrlTemp):
                self._WriteStatus("没有找到有效表单")
                cHttp.Close()
                return
            self._WriteStatus("查找成功，执行后续步骤……")
        else:
            self._WriteStatus("HTTP错误：%d" % (AckCode))
            cHttp.Close()
            return    
        #根据正则表达式填写表单
        cForm.run_id = cRegex.Match(r'RUN_ID=(.*?)&', pszUrlTemp, 1)
        cForm.prcs_id = cRegex.Match(r'PRCS_ID=(.*?)&', pszUrlTemp, 1)
        cForm.flow_prcs = cRegex.Match(r'FLOW_PRCS=(.*?)', pszUrlTemp, 1)
        #cForm.prcs_key_id = cRegex.Match(r'PRCS_KEY_ID=(.*)', pszUrlTemp, 1)
        if (None==cForm.run_id or None==cForm.prcs_id or None==cForm.flow_prcs):
            self._WriteStatus("数据错误：无法获取表单数据")
            return
        
        #Step4：继续获取表单
        if None == pszUrlTemp:
            ReqUrl = "/general/workflow/list/input_form/?MENU_FLAG=&"
            ReqUrl += "RUN_ID=%s&FLOW_ID=%s&PRCS_ID=%s&FLOW_PRCS=%s" % \
                      (cForm.run_id, cForm.flow_id, cForm.prcs_id, cForm.flow_prcs)
        else:
            SplitList = pszUrlTemp.split("../")
            ReqUrl = "/general/workflow/" + SplitList[len(SplitList)-1]

        if (False == cHttp.Send("GET", ReqUrl)):
            self._WriteStatus("发送HTTP请求失败")
            cHttp.Close()
            return
        AckCode, AckHead, AckBody = cHttp.Receive()
        if (200 != AckCode):
            self._WriteStatus("HTTP错误：%d" % (AckCode))
            cHttp.Close()
            return
        #根据正则表达式填写表单
        cForm.prcs_key_id = cRegex.Match(r"prcs_key_id.*?= \'(.*?)\',", AckBody, 1)
        cForm.run_name = cRegex.Match(r"en_run_name.*?=[\s\S]*?run_name.*?= \"(.*?)\"", AckBody, 1)
        if (None == cForm.run_name):
            self._WriteStatus("数据错误：无法获取表单数据")
            cHttp.Close()
            return
        cForm.run_name = urllib.parse.unquote(cForm.run_name)
        cForm.run_name_old = cForm.run_name
        cForm.data_70 = cRegex.Match(r'（(.*?)）(.*?)-(.*)', cForm.run_name, 2)
        cForm.data_68 = cRegex.Match(r'（(.*?)）(.*?)-(.*)', cForm.run_name, 3)
        if None==cForm.data_70 or None==cForm.data_68:
            self._WriteStatus("数据错误：无法获取表单数据")
            return
        #填写加班基本参数
        #TIME
        cForm.data_91 = time.strftime("%Y-%m-%d", time.localtime())
        cForm.data_67 = time.strftime("%X", time.localtime())
        #加班餐
        if (True == self._cConfig.Dinner):
            cForm.data_89 = "是"
        else:
            cForm.data_89 = "否"
        #加班班车
        if (True == self._cConfig.Bus):
            cForm.data_90 = "是"
        else:
            cForm.data_90 = "否"
        #Reason
        cForm.data_73 = self._cConfig.Reason
    
        #Step5：提交当前用户名
        cHttp.SetReqHead("Origin", "http://do.sanhuid.com")
        if (False == cHttp.Send("POST", "/general/workflow/list/input_form/run_name_submit.php", "")):
            self._WriteStatus("发送HTTP请求失败")
            cHttp.Close()
            return
        AckCode, AckHead, AckBody = cHttp.Receive()
        if (200 != AckCode):
            self._WriteStatus("HTTP错误：%d" % (AckCode))
            cHttp.Close()
            return
    
        #Step6：加班申请，组装Body数据
        cHttp.SetReqHead("Cache-Control", "max-age=0")
        cHttp.SetReqHead("Upgrade-Insecure-Requests", "1")
        cHttp.SetReqHead("Content-Type", "multipart/form-data; boundary=%s" % cMime.boundary)
        if (False == cHttp.Send("POST", "/general/workflow/list/input_form/input_submit.php", cMime.AssembleMimeData(False, cForm).encode("GBK"))):
            self._WriteStatus("发送HTTP请求失败")
            cHttp.Close()
            return
        AckCode, AckHead, AckBody = cHttp.Receive()
        if (200 != AckCode):
            self._WriteStatus("HTTP错误：%d" % (AckCode))
            cHttp.Close()
            return
        #警告标志
        Alert = cRegex.Match(r'alert\("(.*?)"\)', AckBody, 1, False)
        if None != Alert:
            self._WriteStatus("提交表单信息错误：%s" % (Alert))
            cHttp.Close()
            return
        #转交成功标志
        if None == AckBody.find(r"\u8f6c\u4ea4\u6210\u529f"):
            self._WriteStatus("提交表单信息错误：未知原因")
            cHttp.Close()
            return
    
        #Step7：第二次提交表单
        if (False == cHttp.Send("POST", "/general/workflow/list/input_form/input_submit.php", cMime.AssembleMimeData(True, cForm).encode("GBK"))):
            self._WriteStatus("发送HTTP请求失败")
            cHttp.Close()
            return
        AckCode, AckHead, AckBody = cHttp.Receive()
        if (200 != AckCode):
            self._WriteStatus("HTTP错误：%d" % (AckCode))
            cHttp.Close()
            return
        
        #Step8：确认加班
        #获取当前时间的毫秒时间戳
        CurMillTime = int(time.time()*1000)
        ReqBody = "_search=false&nd=%s&rows=10&page=1&sidx=run_id&sord=desc" % CurMillTime
        if (False == cHttp.Send("POST", "/general/workflow/list/data/getdata.php?pageType=todo", ReqBody.encode("GBK"))):
            self._WriteStatus("发送HTTP请求失败")
            cHttp.Close()
            return
        AckCode, AckHead, AckBody = cHttp.Receive()
        if (200 != AckCode):
            self._WriteStatus("HTTP错误：%d" % (AckCode))
            cHttp.Close()
            return
    
        #打印日志
        self._WriteStatus("\n一键加班脚本执行完成，请登录网页查看具体信息")
        self._WriteStatus("加班信息：")
        self._WriteStatus("加班时间：%s %s" % (cForm.data_91, cForm.data_67))
        self._WriteStatus("姓名：%s, 部门：%s, 加班餐：%s, 班车：%s, 加班理由：%s" % (cForm.data_68, cForm.data_70, cForm.data_89, cForm.data_90, cForm.data_73))
    
        #Step9：关闭连接
        cHttp.Close()
        
        #Step10:设置一键加班为disable
        self.Btn_AddWork.setEnabled(False)
        
        #更新文件
        if (True == self._cConfig.bUpdate):
            self._cConfig.WriteFile()
        return
    
    def ChangePsw(self):
        pass

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
            
    def _WriteStatus(self, szData):
        self.Edit_Status.appendPlainText(szData)
        QtWidgets.QApplication.processEvents()
        