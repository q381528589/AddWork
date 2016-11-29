# -*- coding: utf-8 -*-

############################################
#����һ���Ӱ�ϵͳ
#������Ҫ�Ľ������
#1.��һ��������룬�����޸�����ʱԶ����֤
#2.����޸����빦�ܣ��޸ķ����������룩
#3.���ӻ�����Ԥ��
############################################

import httplib, urllib
import StringIO, gzip
import re
import random, string
import base64
import time
import os
from DESCode import *
from ConfigFileIO import *

#Cookie��
class CCookie:
    __PhpSessionId = None
    __UserNameCookie = None
    __OAUserId=None
    __SID=None
    __CreakWork="new"
    CookieBuffer = None

    #�������ƣ�CCookie::__init__
    #�������ܣ����캯��
    #�������أ���
    #������������
    def __init__(self):
        pass

    #�������ƣ�CCookie::SetCookie
    #�������ܣ�������Set-Cookie�ֶ�����Ҫ��Cookie������Ӧ�ֶ�
    #�������أ���
    #����������Cookies   ��Cookie����
    def SetCookie(self, Cookies):
        if (None == Cookies):
            return
        #�ָ��ֶ�
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
        #��װCookies
        self.__Assemble()

    #�������ƣ�CCookie::__Assemble
    #�������ܣ���װCookie���ַ���
    #�������أ���װ����ַ���
    #������������
    def __Assemble(self):
        #��ʼ��Cookie����
        self.CookieBuffer = ""
        #�������Cookieֵ
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

#HTTP�����շ���
class CHttp:
    #���ӷ���
    __Connect = None
    #��������
    __Method = ""
    #����Url
    __ReqUrl = ""
    #����ͷ��
    __ReqHead = {}
    #����Cookie
    __cCookie = CCookie()
    #����Body
    __ReqBody = ""
    #��Ӧ
    __Response = ""
    #��Ӧ��
    __AckCode = 200
    #��Ӧͷ��
    __AckHead = []
    #��Ӧ����
    __AckBody = ""

    #�������ƣ�CHttp::__init__
    #�������ܣ����캯��
    #�������أ���
    #������������
    def __init__(self):
        self.__ReqHead = {"Host":"do.sanhuid.com"
            , "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            , "Origin":"http://do.sanhuid.com"
            , "Upgrade-Insecure-Requests":"1"
            , "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/5.7.15319.202 Safari/537.36"
            , "Content-Type":"application/x-www-form-urlencoded"
            , "Accept-Encoding":"gzip, deflate"
            , "Accept-Language":"zh-CN,zh;q=0.8"}

    #�������ƣ�CHttp::SetReqHead
    #�������ܣ����/�޸�����ͷ������
    #�������أ���
    #����������Key       ���ֵ�Key���ֶ�����
    #����������Value     ���ֵ�Value���ֶβ���
    def SetReqHead(self, Key, Value):
        self.__ReqHead.setdefault(Key, Value)

    #�������ƣ�CHttp::DelReqHead
    #�������ܣ�ɾ������ͷ������
    #�������أ���
    #����������Key       ���ֵ�Key���ֶ�����
    def DelReqHead(self, Key):
        del self.__ReqHead[Key]

    #�������ƣ�CHttp::Connect
    #�������ܣ����ӷ�����
    #�������أ�True�ɹ���Falseʧ��
    #����������IpAddr    ��������IP��ַ
    #����������Port      ���������˿ڣ�Ĭ��Ϊ80
    def Connect(self, IpAddr, Port=80):
        self.__Connect = httplib.HTTPConnection(IpAddr, Port)

    #�������ƣ�CHttp::Send
    #�������ܣ�����HTTP����
    #�������أ�True�ɹ���Falseʧ��
    #����������Method    ����������
    #����������ReqUrl    ������URL
    #����������ReqBody   ��������
    def Send(self, Method, ReqUrl, ReqBody=None):
        #���������Ч��
        if None==Method or None==ReqUrl:
            print ("����HTTP����ʱ���������ͻ�Url��Ч")
            return False
        if 0 == len(self.__ReqHead):
            print ("����HTTP����ʱ������ͷ��û���κ�����")
            return False
        #��������ӡ����
        self.__Method = Method
        self.__ReqUrl = ReqUrl
        self.__ReqBody = ReqBody
        print ("%s %s HTTP/1.1") % (Method, ReqUrl)
        #����cookie�ֶε�ReqHead
        if None!=self.__cCookie.CookieBuffer:
            self.SetReqHead("Cookie", self.__cCookie.CookieBuffer)

        #���ݲ�ͬ���ͷ�����������
        try:
            if "POST" == Method:
                self.__Connect.request(method=Method, url=ReqUrl,body=ReqBody, headers=self.__ReqHead)
            if "GET" == Method:
                self.__Connect.request(method=Method, url=ReqUrl, headers=self.__ReqHead)
        except:
            print ("����HTTP��������ʧ��")
            return False

        return True;

    #�������ƣ�CHttp::Receive
    #�������ܣ�����HTTP��Ӧ
    #�������أ�AckCode   ����Ӧ�룬���󷵻�0
    #�������أ�AckHead   ����Ӧͷ�������󷵻�None
    #�������أ�AckBody   ����Ӧ�壬���󷵻�None
    #������������
    def Receive(self):
        try:
            self.__Response = self.__Connect.getresponse()
        except:
            print ("����HTTP��Ӧʧ��")
            return 0, None, None
        self.__AckCode = self.__Response.status
        self.__AckHead = self.__Response.getheaders()
        self.__cCookie.SetCookie(self.__Response.getheader("set-cookie"))
        self.__AckBody = self.__Response.read()
        return self.__AckCode, self.__AckHead, self.__AckBody
    
    #�������ƣ�CHttp::Close
    #�������ܣ��ر�Http����
    #�������أ���
    #������������
    def Close(self):
        self.__Connect.close()

#��ѹ��
class CUnzip:
    __gziper = ""

    #�������ƣ�CUnzip::__init__
    #�������ܣ����캯��
    #�������أ���
    #������������
    def __init__(self):
        pass

    #�������ƣ�CCookie::Decompress
    #�������ܣ���ѹgzip����
    #�������أ���ѹ������
    #����������SrcData       ����ѹǰ����
    def Decompress(self, SrcData):
        compressedstream = StringIO.StringIO(SrcData)
        __gziper = gzip.GzipFile(fileobj=compressedstream)
        #��ȡ��ѹ��������
        DstData = __gziper.read()
        return DstData

#����
class CForm:
    run_name_old = ""
    run_id = ""
    run_name = ""
    flow_id = "131"
    prcs_id = ""
    flow_prcs = ""
    prcs_key_id=""
    #ʱ�䣺ʱ����
    data_67 = ""
    #����
    data_68 = ""
    #����
    data_70 = ""
    #�Ӱ�����
    data_73 = ""
    #�Ӱ��
    data_89 = "��"
    #�೵
    data_90 = "��"
    #���ڣ�������
    data_91 = ""

    #�������ƣ�CForm::__init__
    #�������ܣ����캯��
    #�������أ���
    #������������
    def __init__(self):
        pass

#����ƥ����
class CRegex:
    #�������ƣ�CRegex::__init__
    #�������ܣ����캯��
    #�������أ���
    #������������
    def __init__(self):
        pass

    #�������ƣ�CRegex::Match
    #�������ܣ�������ʽƥ��
    #�������أ�ƥ�䵽������
    #����������Regex        ��������ʽ
    #����������Data         ��ԭʼ����
    #����������Position     ����ȡλ��
    #����������bPrintError  ���Ƿ��ӡ������Ϣ
    def Match(self, Regex, Data, Position, bPrintError=True):
        RegexResult = re.search(Regex, Data, re.M|re.I)
        if None == RegexResult:
            if True == bPrintError:
                print ("������ʽ�������û��ƥ�䵽����")
            return None

        if None == RegexResult.group(Position):
            if True == bPrintError:
                print ("�������ȡλ����������ʽ����")
            return None

        return RegexResult.group(Position)

#MIME��
class CMIME:
    boundary = "----WebKitFormBoundary"
    __CharList = []
    __Buffer = ""

    #�������ƣ�CMIME::__init__
    #�������ܣ����캯��
    #�������أ���
    #������������
    def __init__(self):
        self.__CharList += random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 16)
        self.boundary += string.join(self.__CharList).replace(' ', "")

    #�������ƣ�CMIME::AssembleMimeData
    #�������ܣ���װMIME����
    #�������أ���װ�õ��ַ���
    #����������bAgain    ���Ƿ�Ϊ�ڶ��η���
    #����������cForm     ��������
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
            self.__AddMimeData("SMS_CONTENT", False, "�����ѽ�������ˮ�ţ�%s����������/�ĺţ�%s" % (cForm.run_id, cForm.run_name), False)
            self.__AddMimeData("remind_others_id", False, None, False)
        #���ݽ���
        self.__AddMimeData(None, False, None, True)
        #ת���GBK����
        return self.__Buffer

    #�������ƣ�CMIME::__AddMimeData
    #�������ܣ���װ����MIME����
    #�������أ���
    #����������name      ��Content����
    #����������bAttach   �����ֶ��Ƿ��и�����ɲ���
    #����������Value     ��Content����
    #����������bEnd      ��MIME�Ƿ�ȫ������
    def __AddMimeData(self, name, bAttach, Value, bEnd):
        #��װ��������װMIMEβ������
        if bEnd:
            self.__Buffer += "--%s--\r\n\r\n" % self.boundary
            return

        #�������
        if None == name:
            return

        #MIMEͷ��
        self.__Buffer += "--%s\r\n" % self.boundary
        #Content��������
        self.__Buffer += "Content-Disposition: form-data; name=\"%s\"" % name
        if bAttach:
            self.__Buffer += "; filename=\"\"\r\n"
            self.__Buffer += "Content-Type: application/octet-stream\r\n"
        else:
            self.__Buffer += "\r\n"
        #MIME���ݲ���
        self.__Buffer += "\r\n"
        if None != Value:
            self.__Buffer += "%s\r\n" % Value
        else:
            self.__Buffer += "\r\n"

class CUserInfo:
    #�û���
    UserName = None
    #����
    Password = None
    #�Ƿ�Ӱ��
    Dinner = 1
    #�Ƿ�����೵
    Bus = 0
    #�Ӱ�����
    Reason = ""
    #�����ļ��Ƿ��޸�
    bFileChange = False

    #�������ƣ�CMIME::__init__
    #�������ܣ����캯��
    #�������أ���
    #������������
    def __init__(self, UserName):
        self.UserName = UserName

#�������ƣ�AddWork
#�������ܣ�ִ��һ���Ӱ�
#�������أ�0�ɹ� 1�������� 2������� 3��֤���� 4���Ѵ��� 5�ύ������ 6��������
#����������cUserInfo     ���û���Ϣ
def AddWork(cUserInfo):
    #HTTP�����շ�
    cHttp = CHttp()
    #Gzip���ݽ�ѹ
    cUnZip = CUnzip()
    #�Ӱ��ύ��
    cForm = CForm()
    #������ʽ��
    cRegex = CRegex()
    #MIME��
    cMine = CMIME()
    #��¼�ɹ�����
    SuccessStr = "���ڽ���OAϵͳ�����Ժ�..."
    #ʱ���ʽ����
    TIME_FORMAT = "%X"
    #Url���ݻ���
    pszUrlTemp = None

    #���������Ч��
    if None==cUserInfo.UserName or None==cUserInfo.Password or 0==len(cUserInfo.Reason):
        return 1
    #���ݱ���ת��
    cUserInfo.UserName = cUserInfo.UserName
    cUserInfo.Password = base64.b64encode(cUserInfo.Password)

    #Step1������
    cHttp.Connect("120.27.241.239")

    #Step2����¼
    ReqBody = urllib.urlencode({'UNAME': cUserInfo.UserName, 'PASSWORD': cUserInfo.Password, 'encode_type': 1})
    if False == cHttp.Send("POST", "/logincheck.php", ReqBody):
        return 2
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2
    #��ѹ����
    Data = cUnZip.Decompress(AckBody)
    #��֤��¼���
    Result = Data.find(SuccessStr)
    if -1 == Result:
        print ("�û������������")
        return 3

    #Step3����ȡ��
    cHttp.DelReqHead("Origin")
    cHttp.DelReqHead("Content-Type")
    if False == cHttp.Send("GET", "/general/workflow/new/edit.php?FLOW_ID=%s&AUTO_NEW=1" % cForm.flow_id):
        return 2
    AckCode, AckHead, AckBody = cHttp.Receive()
    #��֤������
    if 302 == AckCode:
        ResData = ""
        for HeadType in AckHead:
            if HeadType[0] == "location":
                ResData = HeadType[1]
    elif 200 == AckCode:
        print ("�½���ʧ�ܣ����ڲ������б����ݡ���")
        #��������
        ReqUrl = "/portal/personal/workflow.php"
        if False == cHttp.Send("GET", ReqUrl):
            return 2
        AckCode, AckHead, AckBody = cHttp.Receive()
        if 200 != AckCode:
            return 2
        ResData = cUnZip.Decompress(AckBody)
        #���ұ����ݡ�����������ʽ
        szRegexTemp = "<td align=\"left\">.*?openURL\(.*?,.*?,'(.*?)'\)\">�Ӱ�Ǽ�"
        szRegexTemp += "��%s��" % time.strftime("%Y��%m��%d��", time.localtime())
        szRegexTemp += ".*?-%s" % cUserInfo.UserName
        pszUrlTemp = cRegex.Match(szRegexTemp, ResData, 1)
        if (None == pszUrlTemp):
            print ("û���ҵ���Ч��")
            return 1
        print ("���ҳɹ�������ִ�к������衭��")
    else:
        print ("���յ���Ӧ����HTTP������Ϊ%d") % AckCode
        return 2
		
    #����������ʽ��д��
    cForm.run_id = cRegex.Match(r'RUN_ID=(.*?)&', ResData, 1)
    cForm.prcs_id = cRegex.Match(r'PRCS_ID=(.*?)&', ResData, 1)
    cForm.flow_prcs = cRegex.Match(r'FLOW_PRCS=(.*?)&', ResData, 1)
    cForm.prcs_key_id = cRegex.Match(r'PRCS_KEY_ID=(.*)', ResData, 1)
    if None==cForm.run_id or None==cForm.prcs_id or None==cForm.flow_prcs or None==cForm.prcs_key_id:
        return 1
    
    #Step4��������ȡ��
    if None == pszUrlTemp:
        ReqUrl = "/general/workflow/list/input_form/?MENU_FLAG=&"
        ReqUrl += "RUN_ID=%s&FLOW_ID=%s&PRCS_ID=%s&FLOW_PRCS=%s&AUTO_NEW=1&PRCS_KEY_ID=%s" % \
                  (cForm.run_id, cForm.flow_id, cForm.prcs_id, cForm.flow_prcs, cForm.prcs_key_id)
    else:
        ReqUrl = pszUrlTemp

    if False == cHttp.Send("GET", ReqUrl):
        return 2
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2
    Data = cUnZip.Decompress(AckBody)
    #����������ʽ��д��
    cForm.run_name = cRegex.Match(r'en_run_name.*?=[\s\S]*?run_name.*?= "(.*?)"', Data, 1)
    if None == cForm.run_name:
        return 1
    cForm.run_name = urllib.unquote(cForm.run_name).decode("utf8").encode("GBK")
    cForm.run_name_old = cForm.run_name
    cForm.data_70 = cRegex.Match(r'��(.*?)��(.*?)-(.*)', cForm.run_name, 2)
    cForm.data_68 = cRegex.Match(r'��(.*?)��(.*?)-(.*)', cForm.run_name, 3)
    if None==cForm.data_70 or None==cForm.data_68:
        return 1
    #��д�Ӱ��������
    #TIME
    cForm.data_91 = time.strftime("%Y-%m-%d", time.localtime())
    cForm.data_67 = time.strftime(TIME_FORMAT, time.localtime())
    #�Ӱ��
    if (True == cUserInfo.Dinner):
        cForm.data_89 = "��"
    else:
        cForm.data_89 = "��"
    #�Ӱ�೵
    if (True == cUserInfo.Bus):
        cForm.data_90 = "��"
    else:
        cForm.data_90 = "��"
    #Reason
    cForm.data_73 = cUserInfo.Reason

    #Step5���ύ��ǰ�û���
    cHttp.SetReqHead("Origin", "http://do.sanhuid.com")
    if False == cHttp.Send("POST", "/general/workflow/list/input_form/run_name_submit.php", ""):
        return 2
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2

    #Step6���Ӱ����룬��װBody����
    cHttp.SetReqHead("Cache-Control", "max-age=0")
    cHttp.SetReqHead("Upgrade-Insecure-Requests", "1")
    cHttp.SetReqHead("Content-Type", "multipart/form-data; boundary=%s" % cMine.boundary)
    cHttp.Send("POST", "/general/workflow/list/input_form/input_submit.php", cMine.AssembleMimeData(False, cForm))
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2
    Data = cUnZip.Decompress(AckBody)
    #�����־
    Alert = cRegex.Match(r'alert\("(.*?)"\)', Data, 1, False)
    if None != Alert:
        print ("�ύ����Ϣ����%s") % Alert
        return 5
    #ת���ɹ���־
    if None == Data.find(r"\u8f6c\u4ea4\u6210\u529f"):
        print ("�ύ����Ϣ����δ֪ԭ��")
        return 5

    #Step7���ڶ����ύ��
    cHttp.Send("POST", "/general/workflow/list/input_form/input_submit.php", cMine.AssembleMimeData(True, cForm))
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2

    #Step8��ȷ�ϼӰ�
    #��ȡ��ǰʱ��ĺ���ʱ���
    CurMillTime = int(time.time()*1000)
    ReqBody = "_search=false&nd=%s&rows=10&page=1&sidx=run_id&sord=desc" % CurMillTime
    cHttp.Send("POST", "/general/workflow/list/data/getdata.php?pageType=todo", ReqBody)
    AckCode, AckHead, AckBody = cHttp.Receive()
    if 200 != AckCode:
        return 2

    #��ӡ��־
    print("һ���Ӱ�ű�ִ����ɣ����¼��ҳ�鿴������Ϣ")
    print("�Ӱ���Ϣ��")
    print("�Ӱ�ʱ�䣺%s %s") % (cForm.data_91, cForm.data_67)
    print("������%s, ���ţ�%s, �Ӱ�ͣ�%s, �೵��%s, �Ӱ����ɣ�%s") % (cForm.data_68, cForm.data_70, cForm.data_89, cForm.data_90, cForm.data_73)
    return 0

    #Step9���ر�����
    cHttp.Close()

#�������ƣ�ReadFile
#�������ܣ���ȡ�����ļ�
#�������أ�0�ɹ� 1���ļ�ʧ�� 2����ʧ�� 3��������
#����������cUserInfo     ���û���Ϣ
#����������cCfgFile      �������ļ���Ϣ
#����������des           ���ӽ�����
def ReadFile(cUserInfo, cCfgFile,  des):
    FileText = cCfgFile.ReadTextFile()
    if None == FileText:
        print ("�������ļ�ʧ��")
        return 1

    #���ݽ���
    DecryptData = des.DESDecode(FileText, cUserInfo.UserName)
    #ȥ��β��'\0'
    DataLen = len(DecryptData)
    for i in range(DataLen, 0, -1):
        if '\0' != DecryptData[DataLen-1]:
            break
        DataLen = DataLen - 1
        DecryptData = DecryptData[:DataLen]
    Couple = DecryptData.split('-')
    if 5 > len(Couple):
        print ("���ݽ���ʧ��")
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

#�������ƣ�ChangeConfig
#�������ܣ��޸������ļ�
#�������أ�True�ɹ���Falseʧ��
#����������cUserInfo		���û���Ϣ
#����������bFirst			���Ƿ��һ����д
#����������bChangePsw		���Ƿ���Ҫ�޸�����
#����������bChangeCfg		���Ƿ���Ҫ�޸�����
def ChangeConfig(cUserInfo, bFirst, bChangePsw=False, bChangeCfg=False):
    if True == bFirst:
        #��������Ȩ
        UserName = raw_input("�������û���: ")
        if UserName != cUserInfo.UserName:
            print ("�û���֤ʧ�ܣ���������ṩ����ϵ~")
            return False
        #����������
        Password = raw_input("����������: ")
        Password2 = raw_input("���ٴ����룺 ")
        if (Password != Password2):
            print ("������������벻ͬ")
            return False
        #��������
        cUserInfo.Password = Password
        #��Ӳ���
        bChangeCfg = True

    if True == bChangePsw:
        #������ԭ����
        Password = raw_input("������ԭ����: ")
        if (Password != cUserInfo.Password):
            print ("�������")
            return False
        #������������
        Password = raw_input("������������: ")
        Password2 = raw_input("���ٴ����룺 ")
        if (Password != Password2):
            print ("������������벻ͬ")
            return False
        #��������
        cUserInfo.Password = Password

    if True == bChangeCfg:
        #�Ƿ���Ҫ�Ӱ��
        Dinner = raw_input("�Ƿ���Ҫ�Ӱ��(1��2��): ")
        if '1' == Dinner:
            cUserInfo.Dinner = 1
        elif '2' == Dinner:
            cUserInfo.Dinner = 0
        else:
            print ("����Ĳ�������ȷ")
            return False
        #�Ƿ���Ҫ�Ӱ�೵
        Bus = raw_input("�Ƿ���Ҫ�Ӱ�೵(1��2��): ")
        if '1' == Bus:
            cUserInfo.Bus = 1
        elif '2' == Bus:
            cUserInfo.Bus = 0
        else:
            print ("����Ĳ�������ȷ")
            return False
        #�Ӱ�����
        cUserInfo.Reason = raw_input("�Ӱ�����: ")

    print ("�޸����óɹ�")
    cUserInfo.bFileChange = True
    return True

#�������ƣ�SaveFile
#�������ܣ����������ļ�
#�������أ���
#����������cUserInfo     ���û���Ϣ
#����������cCfgFile      �������ļ���Ϣ
#����������des           ���ӽ�����
def SaveFile(cUserInfo, cCfgFile, des):
    if False == cUserInfo.bFileChange:
        return

    if None==cUserInfo.UserName or None==cUserInfo.Password or 0==len(cUserInfo.Reason):
        return

    #���浽�ļ�
    Data = cUserInfo.UserName + '-' + cUserInfo.Password + '-'
    if cUserInfo.Dinner:
        Data += '1-'
    else:
        Data += '0-'

    if cUserInfo.Bus:
        Data += '1-'
    else:
        Data += '0-'
    Data += cUserInfo.Reason

    EncryptData = des.DESEncode(Data, cUserInfo.UserName)
    cCfgFile.WriteTextFile(EncryptData)
    #���ò��������޸�ΪFalse
    cUserInfo.bFileChange = False

if __name__ == "__main__":
    #�û�������
    UserName = "Ǯ�λ�"
    #�������ؽ��
    FuncResult = 0
    #�û��Ӱ���Ϣ
    cUserInfo = CUserInfo(UserName)
    #�����ļ�
    cCfgFile = CFileMng("./AddWork.cfg")
    #�ӽ��ܹ���
    des = CDesCode()
    #���ݻ���
    szTemp = ""

    while True:
        #��ȡ�ļ�
        FuncResult = ReadFile(cUserInfo, cCfgFile, des)
        if 0!=FuncResult or UserName!=cUserInfo.UserName:
            if False == ChangeConfig(cUserInfo, True):
				print ("��������˳�...")
				Result = raw_input()
				break
            SaveFile(cUserInfo, cCfgFile, des)

        #����
        osClear = os.system("cls")
        #��ӡ�ļ���ѯ��
        print("\n*********************************************************")
        print ("��ӭʹ�ú�������һ���Ӱ�ű���")
        print ("��ǰ�û���: %s\n") % UserName
        print ("��ѡ������ѡ�")
        print ("1.ִ��һ���Ӱ����")
        print ("2.�޸ı��ر�������(���޸ĵ�¼��������������룡)")
        print ("3.�鿴�û���Ϣ")
        print ("4.�޸ļӰ����")
        print ("5.ɾ�������ļ�")
        print ("6.�˳�����")
        print("*********************************************************")
        #�������
        Input = raw_input()
        #����ѡ��ִ����س���
        if '1' == Input:
            #��֤����
            Password = raw_input("�����뱾�ر��������: ")
            if (Password != cUserInfo.Password):
                print ("�������")
                Result = raw_input()
                continue
            #ִ�мӰ����,���ܳɹ���ʧ�ܣ���ֱ�ӱ����˳�
            AddWork(cUserInfo)
            SaveFile(cUserInfo, cCfgFile, des)
            print ("��������˳�...")
            Result = raw_input()
            break

        elif '2' == Input:
            ChangeConfig(cUserInfo, False, True, False)
            SaveFile(cUserInfo, cCfgFile, des)
            Result = raw_input()
            continue

        elif '3' == Input:
            szTemp = "�û���: %s, " % cUserInfo.UserName
            szTemp += "�Ӱ��: "
            szTemp += "��, " if 1==cUserInfo.Dinner else "��, "
            szTemp += "�Ӱ�೵:"
            szTemp += "��, " if 1==cUserInfo.Bus else "��, "
            szTemp += "�Ӱ�����: %s" % cUserInfo.Reason
            print (szTemp)
            Result = raw_input()
            continue

        elif '4' == Input:
            #��֤����
            Password = raw_input("�����뱾�ر��������: ")
            if (Password != cUserInfo.Password):
                print ("�������")
                continue
            ChangeConfig(cUserInfo, False, False, True)
            SaveFile(cUserInfo, cCfgFile, des)
            Result = raw_input()
            continue

        elif '5' == Input:
            #��֤����
            Password = raw_input("�����뱾�ر��������: ")
            if (Password != cUserInfo.Password):
                print ("�������")
                continue
            cCfgFile.DelTextFile()
            print ("ɾ�������ļ��ɹ�")
            Result = raw_input()
            continue

        elif '6' == Input:
            print ("��������˳�...")
            Result = raw_input()
            break
        
        else:
            print ("������Ч")
            Result = raw_input()
            continue