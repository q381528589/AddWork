#三汇一键加班系统

# -*- coding: utf-8 -*-

import sys
import httplib, urllib
import base64
import StringIO, gzip
import re
import time

#基本参数
username = "钱嘉欢"
password = "sh88861158"
bus = 0
reason = "加班"
boundary="----WebKitFormBoundaryaitCKZqFKOlOn5nd"

#数据编码
username = username.decode("utf8").encode("GBK")
password = base64.b64encode(password)

#Cookie缓存类
class CCookie:
    PhpSessionId = ""
    UserNameCookie = ""
    OAUserId=""
    SID=""
    CreakWork="new"
    Temp = ""

    def __init__(self):
        pass

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
                    self.PhpSessionId = FieldList[1]
                if ("USER_NAME_COOKIE" == FieldList[0]):
                    self.UserNameCookie = FieldList[1]
                if ("OA_USER_ID" == FieldList[0]):
                    self.OAUserId = FieldList[1]
                if (-1 != FieldList[0].find("SID_")):
                    self.SID = FieldList[1]

    def Assemble(self):
        self.Temp = self.Temp + "PHPSESSID=" + self.PhpSessionId + "; "
        self.Temp = self.Temp + "USER_NAME_COOKIE=" + self.UserNameCookie + "; "
        self.Temp = self.Temp + "OA_USER_ID=" + self.OAUserId + "; "
        self.Temp = self.Temp + "SID_" + self.OAUserId + "=" + self.SID + "; "
        self.Temp = self.Temp + "creat_work=" + self.CreakWork
        return self.Temp

#加班表单填表数据
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

    def __init__(self):
        pass

#Http类
class CHttp:
    cCookie = CCookie()
    response = ""
    ReqBody = ""
    ReqUrl = ""
    ReqHeader = ""

    def __init__(self, ReqBody, ReqUrl, ReqHeader):
        self.ReqBody = ReqBody
        self.ReqUrl = ReqUrl
        self.ReqHeader = ReqHeader

    def SendReq(self, conn, method):
        if "POST" == method:
            conn.request(method="POST",url=self.ReqUrl,body=self.ReqBody,headers=self.ReqHeader)
        if "GET" == method:
            conn.request(method="GET",url=self.ReqUrl,headers=self.ReqHeader)

    def RecvRes(self, conn):
        self.response = conn.getresponse()
        ResData = self.response.read()
        self.cCookie.SetCookie(self.response.getheader("set-cookie"))
        return ResData

    def RecvHeader(self, conn, DataType):
        self.RecvRes(conn)
        return self.response.getheader(DataType)

    def Assemble(self):
        return self.cCookie.Assemble()


#解压类
class CUnzip:
    __gziper = ""

    def __init__(self):
        pass

    def Decompress(self, SrcData):
        compressedstream = StringIO.StringIO(SrcData)
        __gziper = gzip.GzipFile(fileobj=compressedstream)
        #读取解压缩后数据
        DstData = __gziper.read()
        return DstData

def GetWorkBody(cForm, bAgain):
    Data = "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"PRCS_TO\"\r\n"
    Data += "\r\n"
    if (1 == bAgain):
        Data += "0,\r\n"
    else:
        Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"webtype\"\r\n"
    Data += "\r\n"
    Data += "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/5.7.15319.202 Safari/537.36\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"PRCS_CHOOSE\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"RUN_PRCS_NAME\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"next_prcs_num\"\r\n"
    Data += "\r\n"
    if (1 == bAgain):
        Data += "0\r\n"
    else:
        Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"info_str\"\r\n"
    Data += "\r\n"
    if (1 == bAgain):
        Data += "0,0,0,1,0,0,0,0,0,\r\n"
    else:
        Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"Symbol\"\r\n"
    Data += "\r\n"
    Data += "0" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"run_name_old\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.run_name_old
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"target\"\r\n"
    Data += "\r\n"
    Data += "parent" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"callback\"\r\n"
    Data += "\r\n"
    Data += "turnCallback" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"SAVE_FLAG\"\r\n"
    Data += "\r\n"
    if (1 == bAgain):
        Data += "tok\r\n"
    else:
        Data += "t\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"FLOW_TYPE\"\r\n"
    Data += "\r\n"
    Data += "1" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"EDIT_MODE\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"RUN_ID\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.run_id
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"RUN_NAME\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.run_name
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"FLOW_ID\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.flow_id
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"PRCS_ID\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.prcs_id
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"FLOW_PRCS\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.flow_prcs
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ITEM_ID_MAX\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"MENU_FLAG\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"HIDDEN_STR\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"READ_ONLY_STR\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"TOP_FLAG_OLD\"\r\n"
    Data += "\r\n"
    Data += "0" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"BACK_CONTENT\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"FLOW_PRCS_LAST\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"PRCS_KEY_ID\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.prcs_key_id
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"work_level\"\r\n"
    Data += "\r\n"
    Data += "0" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"work_level_old\"\r\n"
    Data += "\r\n"
    Data += "0" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"getdata_search\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"sign_object\"\r\n"
    Data += "\r\n"
    Data += "0" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"onekey_next_flag\"\r\n"
    Data += "\r\n"
    Data += "0" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DATA_67\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.data_67
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DATA_68\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.data_68
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DATA_70\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.data_70
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DATA_91\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.data_91
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DATA_89\"\r\n"
    Data += "\r\n"
    Data += "是" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DATA_90\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.data_90
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DATA_73\"\r\n"
    Data += "\r\n"
    Data += "%s\r\n" % cForm.data_73
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"FLOW_AUTO_NUM\"\r\n"
    Data += "\r\n"
    Data += "0" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACHMENT_0\"; filename=\"\"\r\n"
    Data += "Content-Type: application/octet-stream\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACH_NAME\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACH_DIR\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DISK_ID\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACH_PRIV\"\r\n"
    Data += "\r\n"
    Data += "1" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACHMENT_ID_OLD\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACHMENT_NAME_OLD\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"NEW_TYPE\"\r\n"
    Data += "\r\n"
    Data += "doc" + "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"NEW_NAME\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"TD_HTML_EDITOR_CONTENT\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACHMENT1_0\"; filename=\"\"\r\n"
    Data += "Content-Type: application/octet-stream\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACH_NAME1\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"ATTACH_DIR1\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"DISK_ID1\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    Data += "--%s\r\n" % boundary
    Data += "Content-Disposition: form-data; name=\"SIGN_DATA\"\r\n"
    Data += "\r\n"
    Data += "\r\n"
    if (1 == bAgain):
        Data += "--%s\r\n" % boundary
        Data += "Content-Disposition: form-data; name=\"SMS_CONTENT\"\r\n"
        Data += "\r\n"
        Data += "工作已结束，流水号：%s，工作名称/文号：%s\r\n" % (cForm.run_id, cForm.run_name)
        Data += "--%s\r\n" % boundary
        Data += "Content-Disposition: form-data; name=\"remind_others_id\"\r\n"
        Data += "\r\n"
        Data += "\r\n"
    Data += "--%s--\r\n" % boundary
    Data += "\r\n"
    return Data.decode("utf8").encode("GBK")

if __name__ == "__main__":
    #Http登录头部定义
    ReqBody = urllib.urlencode({'UNAME': username, 'PASSWORD': password, 'encode_type': 1})
    ReqUrl = "/logincheck.php"
    ReqHeader = {"Host":"do.sanhuid.com"
                , "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                , "Origin":"http://do.sanhuid.com"
                , "Upgrade-Insecure-Requests":"1"
                , "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/5.7.15319.202 Safari/537.36"
                , "Content-Type":"application/x-www-form-urlencoded"
                , "Accept-Encoding":"gzip, deflate"
                , "Accept-Language":"zh-CN,zh;q=0.8"}
    #解压缩头部定义
    cUnzip = CUnzip()
    #登录成功定义
    SuccessStr = "正在进入OA系统，请稍候..."
    #加班提交表单类定义
    cForm = CForm()
    #时间格式定义
    TIME_FORMAT = "%X"

    #发送数据
    cHttp = CHttp(ReqBody, ReqUrl, ReqHeader);
    conn = httplib.HTTPConnection("120.27.241.239")
    cHttp.SendReq(conn, "POST")
    #接收数据
    ResData = cHttp.RecvRes(conn)
    #解压数据
    Data = cUnzip.Decompress(ResData).decode("GBK").encode("utf8")
    #匹配数据
    Result = Data.find(SuccessStr)
    if -1 == Result:
        print ("用户名或密码错误")
        sys.exit()

    #组装Cookie
    Cookie = cHttp.Assemble()
    cHttp.ReqHeader.setdefault("Cookie", Cookie)

    #获取加班表单数据
    cHttp.ReqUrl = "/general/workflow/new/edit.php?FLOW_ID=%s&AUTO_NEW=1" % cForm.flow_id
    del cHttp.ReqHeader["Origin"]
    del cHttp.ReqHeader["Content-Type"]
    cHttp.SendReq(conn, "GET")
    ResData = cHttp.RecvHeader(conn, "location")
    #根据正则表达式查找对应字段
    if None == ResData:
        print ("申请加班失败：表单已有记录")
        sys.exit()
    ResData = ResData.decode("GBK").encode("utf8")
    #RUN_ID
    RegexResult = re.search(r'RUN_ID=(.*?)&', ResData, re.I)
    cForm.run_id = RegexResult.group(1)
    #PRCS_ID
    RegexResult = re.search(r'PRCS_ID=(.*?)&', ResData, re.I)
    cForm.prcs_id = RegexResult.group(1)
    #FLOW_PRCS
    RegexResult = re.search(r'FLOW_PRCS=(.*?)&', ResData, re.I)
    cForm.flow_prcs = RegexResult.group(1)
    #PRCS_KEY_ID
    RegexResult = re.search(r'PRCS_KEY_ID=(.*)', ResData, re.I)
    cForm.prcs_key_id = RegexResult.group(1)
    if (None==cForm.run_id or None==cForm.prcs_id or None==cForm.flow_prcs or None==cForm.prcs_key_id):
        print ("请求失败")
        sys.exit();
    #再次请求
    cHttp.ReqUrl = "/general/workflow/list/input_form/?MENU_FLAG=&"
    cHttp.ReqUrl += "RUN_ID=%s&FLOW_ID=%s&PRCS_ID=%s&FLOW_PRCS=%s&AUTO_NEW=1&PRCS_KEY_ID=%s" % \
                   (cForm.run_id, cForm.flow_id, cForm.prcs_id, cForm.flow_prcs, cForm.prcs_key_id)
    cHttp.SendReq(conn, "GET")
    ResData = cHttp.RecvRes(conn)
    Data = cUnzip.Decompress(ResData).decode("GBK").encode("utf8")
    #RUN_NAME; RUN_NAME_OLD
    RegexResult = re.search(r'en_run_name.*?=[\s\S]*?run_name.*?= "(.*?)"', Data, re.M|re.I)
    cForm.run_name = urllib.unquote(RegexResult.group(1))
    cForm.run_name_old = cForm.run_name
    #NAME; GROUP; DATE
    RegexResult = re.search(r'（(.*?)）(.*?)-(.*)', cForm.run_name, re.I)
    cForm.data_70 = RegexResult.group(2)
    cForm.data_68 = RegexResult.group(3)

    #填写加班基本参数
    #TIME
    cForm.data_91 = time.strftime("%Y-%m-%d", time.localtime())
    cForm.data_67 = time.strftime(TIME_FORMAT, time.localtime())
    #have_dinner
    cForm.data_89 = "是"
    #take_bus
    if (1 == bus):
        cForm.data_90 = "是"
    else:
        cForm.data_90 = "否"
    #Reason
    cForm.data_73 = reason

    #提交当前用户名
    cHttp.ReqUrl = "/general/workflow/list/input_form/run_name_submit.php"
    cHttp.ReqHeader.setdefault("Origin", "http://do.sanhuid.com")
    cHttp.ReqBody = ""
    cHttp.SendReq(conn, "POST")
    ResData = cHttp.RecvRes(conn)

    #加班申请，组装Body数据
    cHttp.ReqUrl = "/general/workflow/list/input_form/input_submit.php"
    cHttp.ReqHeader.setdefault("Cache-Control", "max-age=0")
    cHttp.ReqHeader.setdefault("Upgrade-Insecure-Requests", "1")
    cHttp.ReqHeader.setdefault("Content-Type", "multipart/form-data; boundary=%s" % boundary)
    cHttp.ReqBody = GetWorkBody(cForm, 0)
    cHttp.SendReq(conn, "POST")
    ResData = cHttp.RecvRes(conn)

    #第二次提交表单
    cHttp.ReqBody = GetWorkBody(cForm, 1)
    cHttp.SendReq(conn, "POST")
    ResData = cHttp.RecvRes(conn)

    #确认加班
    cHttp.ReqUrl = "/general/workflow/list/data/getdata.php?pageType=todo"
    #获取当前时间的毫秒时间戳
    CurMillTime = int(time.time()*1000)
    cHttp.ReqBody = "_search=false&nd=%s&rows=10&page=1&sidx=run_id&sord=desc" % CurMillTime
    cHttp.SendReq(conn, "POST")
    ResData = cHttp.RecvRes(conn)

    #打印日志
    print("一键加班脚本执行完成，请登录网页查看具体信息")
    print("加班信息：")
    print("加班时间：%s") % cForm.data_91
    print("姓名：%s, 部门：%s, 加班餐：%s, 班车：%s, 加班理由：%s") % (cForm.data_68, cForm.data_70, cForm.data_89, cForm.data_90, cForm.data_73)