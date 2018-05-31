# -*- coding: utf-8 -*-

import http.client
from io import StringIO
import gzip
import re
import time
import random, string
import logging

#Cookie类
class CCookie:
    #组装好的cookie
    __m_CookieBuffer = None
    #Cookie字典
    __m_Cookies = {}
    #SID
    __m_SID = ""
    #Cookie有效期
    __m_Expires = 0

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
    def SetCookie(self, AckHead):
        if (0 == len(AckHead)):
            return
        
        #查找Set-Cookie
        for HeadCouple in AckHead:
            if (HeadCouple[0] != "Set-Cookie"):
                continue
            SetCookieList = HeadCouple[1]
            SetCookie = SetCookieList.split('; ')
            for Cookie in SetCookie:
                KVField = Cookie.split('=')
                self.__m_Cookies[KVField[0]] = KVField[1]
                #sid的key值记录下来，方便直接查找
                if (-1 != KVField[0].find("SID_")):
                    self.__m_SID = KVField[0]
                #设置cookie有效期
                if (KVField[0] == "expires"):
                    FormatTime = time.strptime(KVField[1],"%a, %d-%b-%Y %H:%M:%S %Z")
                    self.__m_Expires = time.mktime(FormatTime) + 8*60*60

    #函数名称：CCookie::GetCookieBuffer
    #函数功能：组装Cookie成字符串
    #函数返回：组装后的字符串
    #函数参数：无
    def GetCookieBuffer(self):
        #Cookie超时
        if (time.time()>=self.__m_Expires or 0==len(self.__m_Cookies)):
            self.__m_Cookies = {}
            return None
        
        #初始化Cookie缓存
        self.__m_CookieBuffer = ""
        #依次添加Cookie值
        if ("PHPSESSID" in self.__m_Cookies):
            self.__m_CookieBuffer = self.__m_CookieBuffer + "PHPSESSID=" + self.__m_Cookies["PHPSESSID"] + "; "
        if ("USER_NAME_COOKIE" in self.__m_Cookies):
            self.__m_CookieBuffer = self.__m_CookieBuffer + "USER_NAME_COOKIE=" + self.__m_Cookies["USER_NAME_COOKIE"] + "; "
        if ("OA_USER_ID" in self.__m_Cookies):
            self.__m_CookieBuffer = self.__m_CookieBuffer + "OA_USER_ID=" + self.__m_Cookies["OA_USER_ID"] + "; "
        if ("" != self.__m_SID and self.__m_SID in self.__m_Cookies):
            self.__m_CookieBuffer = self.__m_CookieBuffer + self.__m_SID  + "=" + self.__m_Cookies[self.__m_SID] + "; "
        self.__m_CookieBuffer = self.__m_CookieBuffer + "creat_work=new"

        return self.__m_CookieBuffer

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
    
    #解压缩类
    __cUnZip = None

    #函数名称：CHttp::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        self.__ReqHead = {"Host":"do.sanhuid.com"
            , "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            , "Origin":"http://do.sanhuid.com"
            , "Upgrade-Insecure-Requests":"1"
            , "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
            , "Content-Type":"application/x-www-form-urlencoded"
            , "Accept-Encoding":"gzip, deflate"
            , "Accept-Language":"zh-CN,zh;q=0.8"}
        self.__cUnZip = CUnzip()

    #函数名称：CHttp::SetReqHead
    #函数功能：添加/修改请求头部数据
    #函数返回：无
    #函数参数：Key       ：字典Key，字段类型
    #函数参数：Value     ：字典Value，字段参数
    def SetReqHead(self, Key, Value):
        if (Key in self.__ReqHead):
            self.__ReqHead[Key] = Value
        else:
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
    #函数参数：Port      ：服务器端口，默认为80
    def Connect(self, Port=80):
        if (None != self.__Connect):
            return
        self.__Connect = http.client.HTTPConnection("120.27.241.239", Port, timeout=30)

    #函数名称：CHttp::Send
    #函数功能：发送HTTP请求
    #函数返回：True成功，False失败
    #函数参数：Method    ：请求类型
    #函数参数：ReqUrl    ：请求URL
    #函数参数：ReqBody   ：请求体
    def Send(self, Method, ReqUrl, ReqBody=None):
        #检测数据有效性
        if (None==Method or None==ReqUrl):
            logging.error("发送HTTP请求时，请求类型或Url无效")
            return False
        if (0 == len(self.__ReqHead)):
            logging.error("发送HTTP请求时，请求头部没有任何数据")
            return False
        #拷贝并打印数据
        self.__Method = Method
        self.__ReqUrl = ReqUrl
        self.__ReqBody = ReqBody
        logging.info("%s %s HTTP/1.1" % (Method, ReqUrl))
        #拷贝cookie字段到ReqHead
        CookieBuffer = self.__cCookie.GetCookieBuffer()
        if (None!=CookieBuffer and ""!=CookieBuffer):
            self.SetReqHead("Cookie", CookieBuffer)

        #根据不同类型发送请求数据
        try:
            if ("POST" == Method):
                self.__Connect.request(method=Method, url=ReqUrl,body=ReqBody, headers=self.__ReqHead)
            if ("GET" == Method):
                self.__Connect.request(method=Method, url=ReqUrl, headers=self.__ReqHead)
        except:
            logging.error("发送HTTP请求数据失败")
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
            logging.error("接收HTTP响应失败")
            return 0, None, None
        self.__AckCode = self.__Response.status
        self.__AckHead = self.__Response.getheaders()
        self.__cCookie.SetCookie(self.__AckHead)
        self.__AckBody = self.__Response.read()
        #解压缩
        Encoding = self.__Response.getheader("Content-Encoding")
        if (None!=Encoding and -1!=Encoding.find('gzip')):
            self.__AckBody = self.__cUnZip.Decompress(self.__AckBody)
        
        return self.__AckCode, self.__AckHead, self.__AckBody
    
    #函数名称：CHttp::ValidCookie
    #函数功能：验证cookie是否过期
    #函数返回：True Cookie有效，False Cookie无效
    #函数参数：无
    def ValidCookie(self):
        CookieBuffer = self.__cCookie.GetCookieBuffer()
        if (None!=CookieBuffer and ""!=CookieBuffer):
            return True
        
        return False
            
    #函数名称：CHttp::Close
    #函数功能：关闭Http连接
    #函数返回：无
    #函数参数：无
    def Close(self):
        self.__Connect.close()
        self.__Connect = None

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
        try:  
            DstData = gzip.decompress(SrcData)
            DstData = DstData.decode("GBK")
        except:
            logging.error("gzip解压失败")
            DstData = SrcData
        
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
    #函数参数：bPrintError  ：是否打印错误信息
    def Match(self, Regex, Data, Position, bPrintError=True):
        RegexResult = re.search(Regex, Data, re.M|re.I)
        if None == RegexResult:
            if True == bPrintError:
                logging.error("正则表达式错误或者没有匹配到数据")
            return None

        if None == RegexResult.group(Position):
            if True == bPrintError:
                logging.error("输入的提取位置与正则表达式不符")
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
        szTemp = "".join(self.__CharList).replace(' ', "")
        self.boundary += szTemp

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
        return self.__Buffer

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