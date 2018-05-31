# -*- coding: utf-8 -*-

import urllib, base64
import urllib.request
import time
from HttpInteraction import CHttp, CRegex, CMIME

#错误消息
class CError:
    #错误消息集合
    __m_ErrStr = []
    
    #函数名称：CError::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        self.__m_ErrStr.append("数据无误")
        self.__m_ErrStr.append("参数错误")
        self.__m_ErrStr.append("网络错误")
        self.__m_ErrStr.append("用户名或密码错误")
        self.__m_ErrStr.append("已报名加班")
        self.__m_ErrStr.append("表单已存在")
        self.__m_ErrStr.append("获取表单信息错误")
    
    #函数名称：CError::GetErrMsg
    #函数功能：获取错误解释
    #函数返回：无
    #函数参数：nRet    ：错误码
    def GetErrMsg(self, nRet):
        if (nRet >= len(self.__m_ErrStr)):
            return "传入的返回值错误"
        return self.__m_ErrStr[nRet]
    
#涉及到的Http操作    
class COperation:
    #Http
    __m_cHttp = None
    #正则表达式
    __m_cRegex = CRegex()
    
    #函数名称：COperation::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        self.__m_cHttp = CHttp()
        self.__m_cHttp.Connect()
    
    #函数名称：COperation::CheckUserPsw
    #函数功能：校验用户名和密码
    #函数返回：0正确 1参数错误 2网络错误 3用户名或密码错误
    #函数参数：UserName    :待验证的用户名
    #函数参数：Password    :待验证的密码
    def CheckUserPsw(self, UserName, Password):
        #登录成功定义
        SuccessStr = "正在进入OA系统，请稍候..."
        
        #验证数据有效性
        if (None==UserName or None==Password or ""==UserName or ""==Password):
            return 1
        
        #编码
        UserName = UserName.encode("GBK")
        Password = base64.b64encode(Password.encode("utf-8"))
        
        #尝试连接（若未关闭，会调用HTTP的if函数，非网络错误将不会关闭HTTP会话）
        self.__m_cHttp.Connect()
        #登录的交互过程
        ReqBody = urllib.parse.urlencode({'UNAME': UserName, 'PASSWORD': Password, 'encode_type': 1})
        if (False == self.__m_cHttp.Send("POST", "/logincheck.php", ReqBody)):
            self.__m_cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
        if (200 != AckCode):
            self.__m_cHttp.Close()
            return 2

        #验证登录结果
        Result = AckBody.find(SuccessStr)
        if (-1 == Result):
            return 3
        
        return 0
    
    #函数名称：COperation::CheckAddWork
    #函数功能：检查一键加班情况
    #函数返回：0正确 1参数错误 2网络错误 3用户名或密码错误 4已报名加班
    #函数参数：cConfig    :用户配置
    def CheckAddWork(self, cConfig):
        #检测数据有效性
        if (None==cConfig.UserName or None==cConfig.Password):
            return 1
        
        #维持长链
        self.__m_cHttp.SetReqHead("Connection", "Keep-Alive")
    
        #Step1：连接
        self.__m_cHttp.Connect()
    
        #Step2：登录
        if (False == self.__m_cHttp.ValidCookie()):
            nRet = self.CheckUserPsw(cConfig.UserName, cConfig.Password)
            if (0 != nRet):
                return nRet
        
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
        if (False == self.__m_cHttp.Send("POST", ReqUrl)):
            self.__m_cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
        if (200 != AckCode):
            self.__m_cHttp.Close()
            return 2
        
        szRegexTemp = r"\{[\s]*\"records\"\:[\s]*\"([\d]+)\","
        Result = self.__m_cRegex.Match(szRegexTemp, AckBody.decode("GBK"), 1)
        if (None == Result):
            return 0
        #已报名加班
        if ('0' != Result):
            return 4
        
        return 0

    #函数名称：COperation::AddWork
    #函数功能：一键加班
    #函数返回：0正确 1参数错误 2网络错误 3用户名或密码错误 5表单已存在 6获取表单信息错误
    #函数参数：cForm      :[out]用户信息表单
    #函数参数：cConfig    :用户配置
    #函数参数：bExist     :表单是否存在
    def AddWork(self, cForm, cConfig, bExist=False):
        cMime = CMIME()
        
        #检测数据有效性
        if (None==cConfig.UserName or None==cConfig.Password or 0==len(cConfig.Reason)):
            return 1
        #维持长链
        self.__m_cHttp.SetReqHead("Connection", "Keep-Alive")
    
        #Step1：连接
        self.__m_cHttp.Connect()
    
        #Step2：登录
        if (False == self.__m_cHttp.ValidCookie()):
            nRet = self.__cConfig.CheckUserPsw(self.__cConfig.UserName, self.__cConfig.Password)
            if (0 != nRet):
                return nRet
    
        #Step3：提取表单
        self.__m_cHttp.DelReqHead("Origin")
        self.__m_cHttp.DelReqHead("Content-Type")
        if (False == self.__m_cHttp.Send("GET", \
                    "/general/workflow/new/edit.php?FLOW_ID=%s&AUTO_NEW=1" % cForm.flow_id)):
            self.__m_cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
        #验证表单数据
        pszUrlTemp = None
        if (302 == AckCode):
            for HeadType in AckHead:
                if (HeadType[0] == "location"):
                    pszUrlTemp = HeadType[1]
        elif (200 == AckCode):
            if (False == bExist):
                return 5
            
            #请求数据
            if (False == self.__m_cHttp.Send("GET", "/portal/personal/workflow.php")):
                self.__m_cHttp.Close()
                return 2
            AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
            if (200 != AckCode):
                return 2
            #获取当前系统时间
            cTime = time.localtime()
            #查找表单数据。构建正则表达式
            szRegexTemp = "<td align=\"left\">.*?openURL\(.*?,.*?,'(.*?)'\)\">加班登记"
            szRegexTemp += "（%s年[0]?%s月[0]?%s日）" % (str(cTime.tm_year), str(cTime.tm_mon), str(cTime.tm_mday))
            szRegexTemp += ".*?-%s" % self._cConfig.UserName
            pszUrlTemp = self.__m_cRegex.Match(szRegexTemp, AckBody, 1)
            if (None == pszUrlTemp):
                return 6
        else:
            return 2
        #根据正则表达式填写表单
        cForm.run_id = self.__m_cRegex.Match(r'RUN_ID=(.*?)&', pszUrlTemp, 1)
        cForm.prcs_id = self.__m_cRegex.Match(r'PRCS_ID=(.*?)&', pszUrlTemp, 1)
        cForm.flow_prcs = self.__m_cRegex.Match(r'FLOW_PRCS=(.*?)', pszUrlTemp, 1)
        #cForm.prcs_key_id = cRegex.Match(r'PRCS_KEY_ID=(.*)', pszUrlTemp, 1)
        if (None==cForm.run_id or None==cForm.prcs_id or None==cForm.flow_prcs):
            return 6
        
        #Step4：继续获取表单
        if None == pszUrlTemp:
            ReqUrl = "/general/workflow/list/input_form/?MENU_FLAG=&"
            ReqUrl += "RUN_ID=%s&FLOW_ID=%s&PRCS_ID=%s&FLOW_PRCS=%s" % \
                      (cForm.run_id, cForm.flow_id, cForm.prcs_id, cForm.flow_prcs)
        else:
            SplitList = pszUrlTemp.split("../")
            ReqUrl = "/general/workflow/" + SplitList[len(SplitList)-1]

        if (False == self.__m_cHttp.Send("GET", ReqUrl)):
            self.__m_cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
        if (200 != AckCode):
            return 2
        #根据正则表达式填写表单
        cForm.prcs_key_id = self.__m_cHttp.Match(r"prcs_key_id.*?= \'(.*?)\',", AckBody, 1)
        cForm.run_name = self.__m_cRegex.Match(r"en_run_name.*?=[\s\S]*?run_name.*?= \"(.*?)\"", AckBody, 1)
        if (None == cForm.run_name):
            return 6
        cForm.run_name = urllib.parse.unquote(cForm.run_name)
        cForm.run_name_old = cForm.run_name
        cForm.data_70 = self.__m_cRegex.Match(r'（(.*?)）(.*?)-(.*)', cForm.run_name, 2)
        cForm.data_68 = self.__m_cRegex.Match(r'（(.*?)）(.*?)-(.*)', cForm.run_name, 3)
        if None==cForm.data_70 or None==cForm.data_68:
            return 6
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
        self.__m_cHttp.SetReqHead("Origin", "http://do.sanhuid.com")
        if (False == self.__m_cHttp.Send("POST", "/general/workflow/list/input_form/run_name_submit.php", "")):
            self.__m_cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
        if (200 != AckCode):
            return 2
    
        #Step6：加班申请，组装Body数据
        self.__m_cHttp.SetReqHead("Cache-Control", "max-age=0")
        self.__m_cHttp.SetReqHead("Upgrade-Insecure-Requests", "1")
        self.__m_cHttp.SetReqHead("Content-Type", "multipart/form-data; boundary=%s" % cMime.boundary)
        if (False == self.__m_cHttp.Send("POST", "/general/workflow/list/input_form/input_submit.php", cMime.AssembleMimeData(False, cForm).encode("GBK"))):
            self.__m_cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
        if (200 != AckCode):
            return 2
        #警告标志
        Alert = self.__m_cRegex.Match(r'alert\("(.*?)"\)', AckBody, 1, False)
        if None != Alert:
            return 6
        #转交成功标志
        if None == AckBody.find(r"\u8f6c\u4ea4\u6210\u529f"):
            return 6
    
        #Step7：第二次提交表单
        if (False == self.__m_cHttp.Send("POST", "/general/workflow/list/input_form/input_submit.php", cMime.AssembleMimeData(True, cForm).encode("GBK"))):
            self.__m_cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
        if (200 != AckCode):
            return 2
        
        #Step8：确认加班
        #获取当前时间的毫秒时间戳
        CurMillTime = int(time.time()*1000)
        ReqBody = "_search=false&nd=%s&rows=10&page=1&sidx=run_id&sord=desc" % CurMillTime
        if (False == self.__m_cHttp.Send("POST", "/general/workflow/list/data/getdata.php?pageType=todo", ReqBody.encode("GBK"))):
            self.__m_cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = self.__m_cHttp.Receive()
        if (200 != AckCode):
            return 2
    
        return 0

    #函数名称：COperation::ExitHttp
    #函数功能：退出Http会话
    #函数返回：无
    #函数参数：无    
    def ExitHttp(self):
        self.__m_cHttp.Close()
        return