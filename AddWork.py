# -*- coding: utf-8 -*-

############################################
#三汇一键加班系统
#后期需要改进事项：。
#1.修改配置时需要密码
#2.本地无法读取密码的连接远程验证
############################################

import sys
import httplib, urllib
import StringIO, gzip
import re
import random, string
import base64
import time
from DESCode import *
from ConfigFileIO import *

#Cookie类
class CCookie:
    __PhpSessionId = None
    __UserNameCookie = None
    __OAUserId=None
    __SID=None
    __CreakWork="new"
    CookieBuffer = None

    #函数名称：CCookie::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        pass

    #函数名称：CCookie::SetCookie
    #函数功能：将请求Set-Cookie字段所需要的Cookie填入相应字段
    #函数返回：无
    #函数参数：Cookies   ：Cookie集合
    def SetCookie(self, Cookies):
        if (None == Cookies):
            return
        #分割字段
        SetCookieList = Cookies.split(', ')
        for SetCookie in SetCookieList:
            CookieList = SetCookie.split('; ')
            for Cookie in CookieList:
                FieldList = Cookie.split('=')
                if ("PHPSESSID" == FieldList[0]):
                    self.__PhpSessionId = FieldList[1]
                elif ("USER_NAME_COOKIE" == FieldList[0]):
                    self.__UserNameCookie = FieldList[1]
                elif ("OA_USER_ID" == FieldList[0]):
                    self.__OAUserId = FieldList[1]
                elif (-1 != FieldList[0].find("SID_")):
                    self.__SID = FieldList[1]
        #组装Cookies
        self.__Assemble()

    #函数名称：CCookie::__Assemble
    #函数功能：组装Cookie成字符串
    #函数返回：组装后的字符串
    #函数参数：无
    def __Assemble(self):
        #初始化Cookie缓存
        self.CookieBuffer = ""
        #依次添加Cookie值
        if None!=self.__PhpSessionId:
            self.CookieBuffer = self.CookieBuffer + "PHPSESSID=" + self.__PhpSessionId + "; "
        if None!=self.__UserNameCookie:
            self.CookieBuffer = self.CookieBuffer + "USER_NAME_COOKIE=" + self.__UserNameCookie + "; "
        if None!=self.__OAUserId:
            self.CookieBuffer = self.CookieBuffer + "OA_USER_ID=" + self.__OAUserId + "; "
        if None!=self.__OAUserId and None!=self.__SID:
            self.CookieBuffer = self.CookieBuffer + "SID_" + self.__OAUserId + "=" + self.__SID + "; "
        self.CookieBuffer = self.CookieBuffer + "creat_work=" + self.__CreakWork

        return self.CookieBuffer

#HTTP数据收发类
class CHttp:
    #连接符号
    __Connect = None
    #请求类型
    __Method = ""
    #请求Url
    __ReqUrl = ""
    #请求头部
    __ReqHead = {}
    #请求Cookie
    __cCookie = CCookie()
    #请求Body
    __ReqBody = ""
    #响应
    __Response = ""
    #响应码
    __AckCode = 200
    #响应头部
    __AckHead = []
    #响应数据
    __AckBody = ""

    #函数名称：CHttp::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        self.__ReqHead = {"Host":"do.sanhuid.com"
            , "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            , "Origin":"http://do.sanhuid.com"
            , "Upgrade-Insecure-Requests":"1"
            , "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/5.7.15319.202 Safari/537.36"
            , "Content-Type":"application/x-www-form-urlencoded"
            , "Accept-Encoding":"gzip, deflate"
            , "Accept-Language":"zh-CN,zh;q=0.8"}

    #函数名称：CHttp::SetReqHead
    #函数功能：添加/修改请求头部数据
    #函数返回：无
    #函数参数：Key       ：字典Key，字段类型
    #函数参数：Value     ：字典Value，字段参数
    def SetReqHead(self, Key, Value):
        self.__ReqHead.setdefault(Key, Value)

    #函数名称：CHttp::DelReqHead
    #函数功能：删除请求头部数据
    #函数返回：无
    #函数参数：Key       ：字典Key，字段类型
    def DelReqHead(self, Key):
        del self.__ReqHead[Key]

    #函数名称：CHttp::Connect
    #函数功能：连接服务器
    #函数返回：True成功，False失败
    #函数参数：IpAddr    ：服务器IP地址
    #函数参数：Port      ：服务器端口，默认为80
    def Connect(self, IpAddr, Port=80):
        self.__Connect = httplib.HTTPConnection(IpAddr, Port)

    #函数名称：CHttp::Send
    #函数功能：发送HTTP请求
    #函数返回：True成功，False失败
    #函数参数：Method    ：请求类型
    #函数参数：ReqUrl    ：请求URL
    #函数参数：ReqBody   ：请求体
    def Send(self, Method, ReqUrl, ReqBody=None):
        #检测数据有效性
        if None==Method or None==ReqUrl:
            print ("发送HTTP请求时，请求类型或Url无效")
            return False
        if 0 == len(self.__ReqHead):
            print ("发送HTTP请求时，请求头部没有任何数据")
            return False
        #拷贝并打印数据
        self.__Method = Method
        self.__ReqUrl = ReqUrl
        self.__ReqBody = ReqBody
        print ("%s %s HTTP/1.1") % (Method, ReqUrl)
        #拷贝cookie字段到ReqHead
        if None!=self.__cCookie.CookieBuffer:
            self.SetReqHead("Cookie", self.__cCookie.CookieBuffer)

        #根据不同类型发送请求数据
        try:
            if "POST" == Method:
                self.__Connect.request(method=Method, url=ReqUrl,body=ReqBody, headers=self.__ReqHead)
            if "GET" == Method:
                self.__Connect.request(method=Method, url=ReqUrl, headers=self.__ReqHead)
        except:
            print ("发送HTTP请求数据失败")
            return False

        return True;

    #函数名称：CHttp::Receive
    #函数功能：接收HTTP响应
    #函数返回：AckCode   ：响应码，错误返回0
    #函数返回：AckHead   ：响应头部，错误返回None
    #函数返回：AckBody   ：响应体，错误返回None
    #函数参数：无
    def Receive(self):
        try:
            self.__Response = self.__Connect.getresponse()
        except:
            print ("接收HTTP响应失败")
            return 0, None, None
        self.__AckCode = self.__Response.status
        self.__AckHead = self.__Response.getheaders()
        self.__cCookie.SetCookie(self.__Response.getheader("set-cookie"))
        self.__AckBody = self.__Response.read()
        return self.__AckCode, self.__AckHead, self.__AckBody
    
	#函数名称：CHttp::Close
    #函数功能：关闭Http连接
    #函数返回：无
    #函数参数：无
    def Close(self):
		self.__Connect.close()

#解压类
class CUnzip:
    __gziper = ""

    #函数名称：CUnzip::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        pass

    #函数名称：CCookie::Decompress
    #函数功能：解压gzip数据
    #函数返回：解压后数据
    #函数参数：SrcData       ：解压前数据
    def Decompress(self, SrcData):
        compressedstream = StringIO.StringIO(SrcData)
        __gziper = gzip.GzipFile(fileobj=compressedstream)
        #读取解压缩后数据
        DstData = __gziper.read()
        return DstData

#表单类
class CForm:
    run_name_old = ""
    run_id = ""
    run_name = ""
    flow_id = "131"
    prcs_id = ""
    flow_prcs = ""
    prcs_key_id=""
    #时间：时分秒
    data_67 = ""
    #姓名
    data_68 = ""
    #部门
    data_70 = ""
    #加班理由
    data_73 = ""
    #加班餐
    data_89 = "是"
    #班车
    data_90 = "否"
    #日期：年月日
    data_91 = ""

    #函数名称：CForm::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        pass

#正则匹配类
class CRegex:
    #函数名称：CRegex::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        pass

    #函数名称：CRegex::Match
    #函数功能：正则表达式匹配
    #函数返回：匹配到的数据
    #函数参数：Regex        ：正则表达式
    #函数参数：Data         ：原始数据
    #函数参数：Position     ：提取位置
    def Match(self, Regex, Data, Position):
        RegexResult = re.search(Regex, Data, re.M|re.I)
        if None == RegexResult:
            print ("正则表达式错误或者没有匹配到数据")
            return None
        if None == RegexResult.group(Position):
            print ("输入的提取位置与正则表达式不符")
            return None

        return RegexResult.group(Position)

#MIME类
class CMIME:
    boundary = "----WebKitFormBoundary"
    __CharList = []
    __Buffer = ""

    #函数名称：CMIME::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        self.__CharList += random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 16)
        self.boundary += string.join(self.__CharList).replace(' ', "")

    #函数名称：CMIME::AssembleMimeData
    #函数功能：组装MIME数据
    #函数返回：组装好的字符串
    #函数参数：bAgain    ：是否为第二次发送
    #函数参数：cForm     ：表单数据
    def AssembleMimeData(self, bAgain, cForm):
        if False == bAgain:
            self.__AddMimeData("PRCS_TO", False, None, False)
        else:
            self.__AddMimeData("PRCS_TO", False, "0,", False)
        self.__AddMimeData("webtype", False, "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/5.7.15319.202 Safari/537.36", False)
        self.__AddMimeData("PRCS_CHOOSE", False, None, False)
        self.__AddMimeData("RUN_PRCS_NAME", False, None, False)
        if False == bAgain:
            self.__AddMimeData("next_prcs_num", False, None, False)
        else:
            self.__AddMimeData("next_prcs_num", False, "0", False)

        if False == bAgain:
            self.__AddMimeData("info_str", False, None, False)
        else:
            self.__AddMimeData("info_str", False, "0,0,0,1,0,0,0,0,0,", False)
        self.__AddMimeData("Symbol", False, "0", False)
        self.__AddMimeData("run_name_old", False, cForm.run_name_old, False)
        self.__AddMimeData("target", False, "parent", False)
        self.__AddMimeData("callback", False, "turnCallback", False)
        if False == bAgain:
            self.__AddMimeData("SAVE_FLAG", False, "t", False)
        else:
            self.__AddMimeData("SAVE_FLAG", False, "tok", False)
        self.__AddMimeData("FLOW_TYPE", False, "1", False)
        self.__AddMimeData("EDIT_MODE", False, None, False)
        self.__AddMimeData("RUN_ID", False, "%s" % cForm.run_id, False)
        self.__AddMimeData("RUN_NAME", False, "%s" % cForm.run_name, False)
        self.__AddMimeData("FLOW_ID", False, "%s" % cForm.flow_id, False)
        self.__AddMimeData("PRCS_ID", False, "%s" % cForm.prcs_id, False)
        self.__AddMimeData("FLOW_PRCS", False, "%s" % cForm.flow_prcs, False)
        self.__AddMimeData("ITEM_ID_MAX", False, None, False)
        self.__AddMimeData("MENU_FLAG", False, None, False)
        self.__AddMimeData("HIDDEN_STR", False, None, False)
        self.__AddMimeData("READ_ONLY_STR", False, None, False)
        self.__AddMimeData("TOP_FLAG_OLD", False, "0", False)
        self.__AddMimeData("BACK_CONTENT", False, None, False)
        self.__AddMimeData("FLOW_PRCS_LAST", False, None, False)
        self.__AddMimeData("PRCS_KEY_ID", False, "%s" % cForm.prcs_key_id, False)
        self.__AddMimeData("work_level", False, "0", False)
        self.__AddMimeData("work_level_old", False, "0", False)
        self.__AddMimeData("getdata_search", False, None, False)
        self.__AddMimeData("sign_object", False, "0", False)
        self.__AddMimeData("onekey_next_flag", False, "0", False)
        self.__AddMimeData("DATA_67", False, "%s" % cForm.data_67, False)
        self.__AddMimeData("DATA_68", False, "%s" % cForm.data_68, False)
        self.__AddMimeData("DATA_70", False, "%s" % cForm.data_70, False)
        self.__AddMimeData("DATA_91", False, "%s" % cForm.data_91, False)
        self.__AddMimeData("DATA_89", False, "%s" % cForm.data_89, False)
        self.__AddMimeData("DATA_90", False, "%s" % cForm.data_90, False)
        self.__AddMimeData("DATA_73", False, "%s" % cForm.data_73, False)
        self.__AddMimeData("FLOW_AUTO_NUM", False, "0", False)
        self.__AddMimeData("ATTACHMENT_0", True, None, False)
        self.__AddMimeData("ATTACH_NAME", False, None, False)
        self.__AddMimeData("ATTACH_DIR", False, None, False)
        self.__AddMimeData("DISK_ID", False, None, False)
        self.__AddMimeData("ATTACH_PRIV", False, "1", False)
        self.__AddMimeData("ATTACHMENT_ID_OLD", False, None, False)
        self.__AddMimeData("ATTACHMENT_NAME_OLD", False, None, False)
        self.__AddMimeData("NEW_TYPE", False, "doc", False)
        self.__AddMimeData("NEW_NAME", False, None, False)
        self.__AddMimeData("TD_HTML_EDITOR_CONTENT", False, None, False)
        self.__AddMimeData("ATTACHMENT1_0", True, None, False)
        self.__AddMimeData("ATTACH_NAME1", False, None, False)
        self.__AddMimeData("ATTACH_DIR1", False, None, False)
        self.__AddMimeData("DISK_ID1", False, None, False)
        self.__AddMimeData("SIGN_DATA", False, None, False)
        if True == bAgain:
            self.__AddMimeData("SMS_CONTENT", False, "工作已结束，流水号：%s，工作名称/文号：%s" % (cForm.run_id, cForm.run_name), False)
            self.__AddMimeData("remind_others_id", False, None, False)
        #数据结束
        self.__AddMimeData(None, False, None, True)
        #转码成GBK发送
        return self.__Buffer.decode("utf8").encode("GBK")

    #函数名称：CMIME::__AddMimeData
    #函数功能：组装单个MIME数据
    #函数返回：无
    #函数参数：name      ：Content描述
    #函数参数：bAttach   ：该字段是否有附件组成部分
    #函数参数：Value     ：Content内容
    #函数参数：bEnd      ：MIME是否全部结束
    def __AddMimeData(self, name, bAttach, Value, bEnd):
        #组装结束，加装MIME尾部数据
        if bEnd:
            self.__Buffer += "--%s--\r\n\r\n" % self.boundary
            return

        #参数检测
        if None == name:
            return

        #MIME头部
        self.__Buffer += "--%s\r\n" % self.boundary
        #Content描述部分
        self.__Buffer += "Content-Disposition: form-data; name=\"%s\"" % name
        if bAttach:
            self.__Buffer += "; filename=\"\"\r\n"
            self.__Buffer += "Content-Type: application/octet-stream\r\n"
        else:
            self.__Buffer += "\r\n"
        #MIME内容部分
        self.__Buffer += "\r\n"
        if None != Value:
            self.__Buffer += "%s\r\n" % Value
        else:
            self.__Buffer += "\r\n"
        #MIME结尾标志
        self.__Buffer += "--%s\r\n" % self.boundary

class CUserInfo:
	UserName = None
	Password = None
	Dinner = 1
	Bus = 0
	Reason = None
	bFileChange = False

	#函数名称：CMIME::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
	def __init__(self, UserName):
		self.UserName = UserName

#函数名称：AddWork
#函数功能：执行一键加班
#函数返回：0成功 1参数错误 2网络错误 3认证错误 4表单已存在 5提交表单错误 6其它错误
#函数参数：cUserInfo     ：用户信息
def AddWork(cUserInfo):
    #HTTP数据收发
    cHttp = CHttp()
    #Gzip数据解压
    cUnZip = CUnzip()
    #加班提交表单
    cForm = CForm()
    #正则表达式类
    cRegex = CRegex()
    #MIME类
    cMine = CMIME()
    #登录成功定义
    SuccessStr = "正在进入OA系统，请稍候..."
    #时间格式定义
    TIME_FORMAT = "%X"

    #检测数据有效性
    if None==cUserInfo.UserName or None==cUserInfo.Password or None==cUserInfo.Reason:
        return 1
    #数据编码转换
    cUserInfo.UserName = cUserInfo.UserName.decode("utf8").encode("GBK")
    cUserInfo.Password = base64.b64encode(Password)

    #Step1：连接
    cHttp.Connect("120.27.241.239")

    #Step2：登录
    ReqBody = urllib.urlencode({'UNAME': cUserInfo.UserName, 'PASSWORD': cUserInfo.Password, 'encode_type': 1})
    if False == cHttp.Send("POST", "/logincheck.php", ReqBody):
        return 2
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2
    #解压数据
    Data = cUnZip.Decompress(AckBody).decode("GBK").encode("utf8")
    #验证登录结果
    Result = Data.find(SuccessStr)
    if -1 == Result:
        print ("用户名或密码错误")
        return 3

    #Step3：提取表单
    cHttp.DelReqHead("Origin")
    cHttp.DelReqHead("Content-Type")
    if False == cHttp.Send("GET", "/general/workflow/new/edit.php?FLOW_ID=%s&AUTO_NEW=1" % cForm.flow_id):
        return 2
    AckCode, AckHead, AckBody = cHttp.Receive()
    #验证表单数据
    if 200 == AckCode:
        print ("该表单已存在，开通会员服务即可自动提交未填写完表单")
        print ("由于程序猿太懒，该功能暂未实现，根据打赏金额可考虑实现该功能")
        return 4
    elif 302 != AckCode:
        print ("接收到响应错误，HTTP返回码为%d") % AckCode
        return 2
    ResData = ""
    for HeadType in AckHead:
        if HeadType[0] == "location":
            ResData = HeadType[1]
    #根据正则表达式填写表单
    cForm.run_id = cRegex.Match(r'RUN_ID=(.*?)&', ResData, 1)
    cForm.prcs_id = cRegex.Match(r'PRCS_ID=(.*?)&', ResData, 1)
    cForm.flow_prcs = cRegex.Match(r'FLOW_PRCS=(.*?)&', ResData, 1)
    cForm.prcs_key_id = cRegex.Match(r'PRCS_KEY_ID=(.*?)&', ResData, 1)
    if None==cForm.run_id or None==cForm.prcs_id or None==cForm.flow_prcs or None==cForm.prcs_key_id:
        return 1

    #Step4：继续获取表单
    ReqUrl = "/general/workflow/list/input_form/?MENU_FLAG=&"
    ReqUrl += "RUN_ID=%s&FLOW_ID=%s&PRCS_ID=%s&FLOW_PRCS=%s&AUTO_NEW=1&PRCS_KEY_ID=%s" % \
                   (cForm.run_id, cForm.flow_id, cForm.prcs_id, cForm.flow_prcs, cForm.prcs_key_id)
    if False == cHttp.Send("GET", ReqUrl):
        return 2
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2
    Data = cUnZip.Decompress(AckBody).decode("GBK").encode("utf8")
    #根据正则表达式填写表单
    cForm.run_name = cRegex.Match(r'en_run_name.*?=[\s\S]*?run_name.*?= "(.*?)"', Data, 1)
    if None == cForm.run_name:
        return 1
    cForm.run_name = urllib.unquote(cForm.run_name)
    cForm.run_name_old = cForm.run_name
    cForm.data_70 = cRegex.Match(r'（(.*?)）(.*?)-(.*)', Data, 2)
    cForm.data_68 = cRegex.Match(r'（(.*?)）(.*?)-(.*)', Data, 3)
    if None==cForm.data_70 or None==cForm.data_68:
        return 1
    #填写加班基本参数
    #TIME
    cForm.data_91 = time.strftime("%Y-%m-%d", time.localtime())
    cForm.data_67 = time.strftime(TIME_FORMAT, time.localtime())
    #加班餐
    if (True == cUserInfo.Dinner):
        cForm.data_89 = "是"
    else:
        cForm.data_89 = "否"
    #加班班车
    if (True == cUserInfo.Bus):
        cForm.data_90 = "是"
    else:
        cForm.data_90 = "否"
    #Reason
    cForm.data_73 = cUserInfo.Reason

    #Step5：提交当前用户名
    cHttp.ReqHeader.setdefault("Origin", "http://do.sanhuid.com")
    if False == cHttp.Send("POST", "/general/workflow/list/input_form/run_name_submit.php", ""):
        return 2
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2

    #Step6：加班申请，组装Body数据
    cHttp.ReqHeader.setdefault("Cache-Control", "max-age=0")
    cHttp.ReqHeader.setdefault("Upgrade-Insecure-Requests", "1")
    cHttp.ReqHeader.setdefault("Content-Type", "multipart/form-data; boundary=%s" % cMine.boundary)
    cHttp.Send("POST", "/general/workflow/list/input_form/input_submit.php", cMine.AssembleMimeData(False, cForm))
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2
    Data = cUnZip.Decompress(AckBody).decode("GBK").encode("utf8")
    #转交成功标志
    if None == Data.find("\u8f6c\u4ea4\u6210\u529f"):
        print ("提交的表单信息错误")
        return 5

    #Step7：第二次提交表单
    cHttp.Send("POST", "/general/workflow/list/input_form/input_submit.php", cMine.AssembleMimeData(True, cForm))
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2

    #Step8：确认加班
    #获取当前时间的毫秒时间戳
    CurMillTime = int(time.time()*1000)
    ReqBody = "_search=false&nd=%s&rows=10&page=1&sidx=run_id&sord=desc" % CurMillTime
    cHttp.Send("POST", "/general/workflow/list/data/getdata.php?pageType=todo", ReqBody)
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2

    #打印日志
    print("一键加班脚本执行完成，请登录网页查看具体信息")
    print("加班信息：")
    print("加班时间：%s %s") % (cForm.data_91, cForm.data_67)
    print("姓名：%s, 部门：%s, 加班餐：%s, 班车：%s, 加班理由：%s") % (cForm.data_68, cForm.data_70, cForm.data_89, cForm.data_90, cForm.data_73)
    return 0
	
	#Step9：关闭连接
	cHttp.Close()

#函数名称：ReadFile
#函数功能：读取配置文件
#函数返回：0成功 1打开文件失败 2解密失败 3参数错误
#函数参数：无
def ReadFile(cUserInfo):
	cCfgFile = CFileMng("./AddWork.cfg")
	FileText = cCfgFile.ReadTextFile()
	if None == FileText:
		print ("打开配置文件失败")
		return 1
	
	#数据解密
	des = CDesCode()
	DecryptData = des.DESDecode(FileText, cUserInfo.UserName)
	Couple = DecryptData.split('-')
	if None==Couple[0] or None==Couple[1] or None==Couple[2] or None==Couple[3] or None==Couple[4]:
		print ("数据解密失败")
		return 2
	cUserInfo.UserName = Couple[0]
	cUserInfo.Password = Couple[1]
	if '1' == Couple[2]:
		cUserInfo.Dinner = True
	elif '0' == Couple[2]:
		cUserInfo.Dinner = False
	else:
		return 3
		
	if '1' == Couple[3]:
		cUserInfo.Bus = True
	elif '0' == Couple[3]:
		cUserInfo.Bus = False
	else:
		return 3
	cUserInfo.Reason = Couple[4]
	
	return 0

#函数名称：ChangeConfig
#函数功能：修改配置文件
#函数返回：True成功，False失败
#函数参数：cUserInfo		：用户信息
#函数参数：bFirst			：是否第一次填写
#函数参数：bChangePsw		：是否需要修改密码
#函数参数：bChangeCfg		：是否需要修改配置
def ChangeConfig(cUserInfo, bFirst, bChangePsw=False, bChangeCfg=False):
	if True == bFirst:
		#请输入密码
		Password = input("请输入密码: ")
		Password2 = input("请再次输入： ")
		if (Password != Password2):
			print ("输入的两次密码不同")
			return False
		#保存密码
		cUserInfo.Password = Password
		#添加参数
		bChangeCfg = True
		
	if True == bChangePsw:
		#请输入原密码
		Password = input("请输入原密码: ")
		if (Password != cUserInfo.Password):
			print ("密码错误")
			return False
		#请输入新密码
		Password = input("请输入新密码: ")
		Password2 = input("请再次输入： ")
		if (Password != Password2):
			print ("输入的两次密码不同")
			return False
		#保存密码
		cUserInfo.Password = Password
	
	if True == bChangeCfg:
		#是否需要加班餐
		Dinner = input("是否需要加班餐(1是2否): ")
		if '1' == Dinner:
			cUserInfo.Dinner = 1
		elif '0' == Dinner:
			cUserInfo.Dinner = 0
		else:
			print ("输入的参数不正确")
			return False
		#是否需要加班班车
		Bus = input("是否需要加班班车(1是2否): ")
		if '1' == Bus:
			cUserInfo.Bus = 1
		elif '0' == Bus:
			cUserInfo.Bus = 0
		else:
			print ("输入的参数不正确")
			return False
		#加班理由
		cUserInfo.Reason = input("加班理由: ")
		
		print ("修改配置成功")
		bFileChange = True
		return True
	
def SaveFile(cUserInfo):
	if False == cUserInfo.bFileChange:
		return
	
	if None==cUserInfo.UserName or None==cUserInfo.Password or None==None==cUserInfo.Reason:
		return
	
    #保存到文件
	Data = cUserInfo.UserName + "-" + cUserInfo.Password + '-'
	if cUserInfo.Dinner:
		Data += '1-'
	else:
		Data += '0-'

	if cUserInfo.Bus:
		Data += '1-'
	else:
		Data += '0- '
	Data += cUserInfo.Reason

	EncryptData = des.DESEncode(Data, cUserInfo.UserName)
	cCfgFile.WriteTextFile(EncryptData)
	#配置参数重新修改为False
	cUserInfo.bFileChange = False

if __name__ == "__main__":
	UserName = "钱嘉欢"
	cUserInfo = CUserInfo(UserName)
	FuncResult = 0
	
	while True:
		#打印文件并询问
		print ("欢迎进入一键加班系统！")
		print ("当前用户名: %s") % UserName
		print ("请选择以下选项：")
		print ("1.执行一键加班程序")
		print ("2.修改登录密码(仅修改本地密码，不修改登录服务器所需的密码！)")
		print ("3.修改加班参数")
		print ("4.删除配置文件")
		print ("5.退出程序")
		
		#输入参数
		Input = input()
		#根据选择执行相关程序
		if '1' == Input:
			#读取文件
			FuncResult = ReadFile(cUserInfo)
			if 0 == FuncResult:
				#检测程序授权
				if UserName != cUserInfo.UserName:
					print ("该软件没有授权给当前用户，请联系软件开发者，谢谢！")
					sys.exit()
				#执行加班程序,不管成功与失败，均直接保存退出
				AddWork(cUserInfo)
				SaveFile()
				break
			elif 1==FuncResult or 2==FuncResult:
				ChangeConfig(cUserInfo, True)
				continue
			elif 3==FuncResult:
				ChangeConfig(cUserInfo, False, False, True)
				continue
				
		elif '2' == Input:
			ChangeConfig(cUserInfo, False, True, False)
			SaveFile()
			continue
			
		elif '3' == Input:
			ChangeConfig(cUserInfo, False, False, True)
			SaveFile()
			continue

		elif '4' == Input:
			cCfgFile = CFileMng("./AddWork.cfg")
			cCfgFile.DelTextFile()
			print ("删除配置文件成功")
			continue
			
		elif '5' == Input:
			Result = input("输入任意内容后回车退出...")
			break