# -*- coding: utf-8 -*-

import sys
import httplib, urllib
import StringIO, gzip
import re
#from DESCode import *
#from ConfigFileIO import *

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
        pass

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
    #函数返回：AckCode   ：响应码
    #函数返回：AckHead   ：响应头部
    #函数返回：AckBody   ：响应体
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
        self.__ReqBody = self.__Response.read()
        return self.__AckCode, self.__AckHead, self.__AckBody

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
    data_73 = "加班"
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

if __name__ == "__main__":
    #HTTP数据收发
    cHttp = CHttp()
    #Gzip数据解压
    cUnZip = CUnzip()
    #加班提交表单
    cForm = CForm()
    #正则表达式类
    cRegex = CRegex()
    #登录成功定义
    SuccessStr = "正在进入OA系统，请稍候..."

    #Step1：连接
    cHttp.Connect("120.27.241.239")

    #Step2：登录
    cHttp.SetReqHead("Host", "do.sanhuid.com")
    cHttp.SetReqHead("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    cHttp.SetReqHead("Origin", "http://do.sanhuid.com")
    cHttp.SetReqHead("Upgrade-Insecure-Requests", "1")
    cHttp.SetReqHead("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/5.7.15319.202 Safari/537.36")
    cHttp.SetReqHead("Content-Type", "application/x-www-form-urlencoded")
    cHttp.SetReqHead("Accept-Encoding", "gzip, deflate")
    cHttp.SetReqHead("Accept-Language", "zh-CN,zh;q=0.8")
    ReqBody = urllib.urlencode({'UNAME': 'username', 'PASSWORD': 'password', 'encode_type': 1})
    if False == cHttp.Send("POST", "/logincheck.php", ReqBody):
        sys.exit()
    AckCode, AckHead, AckBody = cHttp.Receive()
    #解压数据
    Data = cUnZip.Decompress(AckBody).decode("GBK").encode("utf8")
    #验证登录结果
    Result = Data.find(SuccessStr)
    if -1 == Result:
        print ("用户名或密码错误")
        sys.exit()

    #Step3：提取表单
    cHttp.DelReqHead("Origin")
    cHttp.DelReqHead("Content-Type")
    if False == cHttp.Send("GET", "/general/workflow/new/edit.php?FLOW_ID=%s&AUTO_NEW=1"):
        sys.exit()
    AckCode, AckHead, AckBody = cHttp.Receive()
    #验证表单数据
    if 200 == AckCode:
        print ("该表单已存在，开通会员服务即可自动提交未填写完表单")
        print ("由于程序猿太懒，该功能暂未实现，根据打赏金额可考虑实现该功能")
        sys.exit()
    elif 302!=AckCode:
        print ("接收到响应错误，HTTP返回码为%d") % AckCode
        sys.exit()
    ResData = AckBody.decode("GBK").encode("utf8")
    #RUN_ID
    if None == cRegex.Match(r'RUN_ID=(.*?)&', ResData, 1):
        sys.exit()
    #PRCS_ID
    if None == cRegex.Match(r'PRCS_ID=(.*?)&', ResData, 1):
        sys.exit()
    #FLOW_PRCS
    if None == cRegex.Match(r'FLOW_PRCS=(.*?)&', ResData, 1):
        sys.exit()
    #PRCS_KEY_ID
    if None == cRegex.Match(r'PRCS_KEY_ID=(.*?)&', ResData, 1):
        sys.exit()

    #Step4：继续获取表单