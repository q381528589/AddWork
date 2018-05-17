# -*- coding: utf-8 -*-

import os
import hashlib
from HttpInteraction import CHttp, CUnzip
import urllib, base64
import logging
from builtins import int

#配置文件类
class CConfig:
    #用户名
    UserName = None
    #密码
    Password = None
    #是否加班餐
    Dinner = 1
    #是否乘坐班车
    Bus = 0
    #加班理由
    Reason = ""
    #跳过登录
    bSkip = False
    #配置文件是否被修改
    bFileChange = False
    
    #文件配置类
    _cCfgFile = None
    #加密算法类
    _cDes = None
    #临时成员变量：是否更新加密文件
    bUpdate = False

    #函数名称：CConfig::__init__
    #函数功能：构造函数
    #函数参数：cCfgFile      ：配置文件信息
    #函数参数：des           ：加解密类
    def __init__(self, cCfgFile, des):
        self._cCfgFile = cCfgFile
        self._cDes = des
  
    #函数名称：CConfig::ReadFile
    #函数功能：读取配置文件
    #函数返回：0成功 1打开文件失败 2解密失败 3参数错误
    #函数参数：无
    #函数参数：无
    def ReadFile(self):
        FileText = self._cCfgFile.ReadTextFile()
        if None == FileText:
            logging.error("打开配置文件失败")
            return 1
        
        #V2版本解密
        if ("V3" != FileText[0:2]):
            nRet = self.V2Decrypt(FileText)
        else:
            nRet = self.V3Decrypt(FileText)

        return nRet

    #函数名称：CConfig::WriteFile
    #函数功能：读取配置文件
    #函数返回：0成功 1打开文件失败 2加密失败 3参数错误
    #函数参数：无
    #函数参数：无
    def WriteFile(self):
        #数据缓存
        szTemp = ""
        
        #计算用户名的MD5
        Md5Value = self.CalcMD5(self.UserName)
        if (32 != len(Md5Value)):
            logging.error("数据加密失败：MD5值长度不正确") 
        
        #用户数据编成字符串
        Data = self.UserName + '-' + self.Password + '-'
        if self.Dinner:
            Data += '1-'
        else:
            Data += '0-'
    
        if self.Bus:
            Data += '1-'
        else:
            Data += '0-'
        Data += self.Reason
        
        #跳过密码字段
        szSkip = '1' if self.bSkip else '0'
        Data = Data + '-' + szSkip
        
        try:    
            EncryptData = self._cDes.Encrypt(Data, Md5Value)
            if (None == EncryptData):
                logging.error("数据加密失败：导入的MD5值不正确")
                return 2
        except:
            logging.error("数据加密失败：未知原因")
            return 2
        
        #整理
        szTemp = 'V3' + '032' + Md5Value
        EncryptDataLen = len(EncryptData)
        if (EncryptDataLen < 10):
            szTemp = szTemp + '00' + str(EncryptDataLen)
        elif (EncryptDataLen < 100):
            szTemp = szTemp + '0' + str(EncryptDataLen)
        elif (EncryptDataLen < 1000):
            szTemp = szTemp + str(EncryptDataLen)
        #数据超过预期长度
        else:
            logging.error("数据超过预期长度，请精简加班理由")
            return 3
        szTemp += EncryptData.decode()
        
        #写入文件
        if (False == self._cCfgFile.WriteTextFile(szTemp)):
            return 1
        
        return 0

    #函数名称：CConfig::CalcMD5
    #函数功能：计算MD5
    #函数返回：MD5值
    #函数参数：Data    ：要计算的数据
    def CalcMD5(self, Data):
        #计算数据的MD5
        cMD5 = hashlib.md5(Data.encode(encoding='utf-8'))
        #cMD5.update(Data)
        Md5Value = cMD5.hexdigest()
        return Md5Value

    #函数名称：CConfig::V2Decrypt
    #函数功能：V2版本解密
    #函数返回：解密后的消息
    #函数参数：FileText：读取的文件内容
    def V2Decrypt(self, FileText):
        #分割字串
        EncryptData = FileText.split(' ')
        if (3 > len(EncryptData)):
            logging.error("数据解密失败:文件内容未找到有效分割点")
            return 2
        #读取用户名的MD5
        UserMD5 = EncryptData[0]
                    
        #数据解密
        try:
            DecryptData = self._cDes.Decrypt(EncryptData[1], UserMD5)
            if (None == DecryptData):
                logging.error("数据解密失败：导入的MD5值不正确")
                return 2
        except:
            logging.error("数据解密失败：未知原因")
            return 2
        
        #对解密后的数据进行分割
        Couple = DecryptData.split('-')
        if 5 > len(Couple):
            logging.error("数据解密失败：解密后的数据不符合要求")
            return 2
        self.UserName = Couple[0]
        self.Password = Couple[1]
        if '1' == Couple[2]:
            self.Dinner = True
        elif '0' == Couple[2]:
            self.Dinner = False
        else:
            return 3
    
        if '1' == Couple[3]:
            self.Bus = True
        elif '0' == Couple[3]:
            self.Bus = False
        else:
            return 3
        self.Reason = Couple[4]
        #验证用户名
        Md5Value = self.CalcMD5(self.UserName)
        if (Md5Value != EncryptData[0]):
            logging.error("数据解密失败：MD5值校验不通过")
            return 3
        
        #是否跳过登录
        if ('1' == EncryptData[2]):
            self.bSkip = True
    
        self.bUpdate = True
        return 0

    #函数名称：CConfig::V3Decrypt
    #函数功能：V2版本解密
    #函数返回：解密后的消息
    #函数参数：FileText：读取的文件内容
    def V3Decrypt(self, FileText):
        #数据缓存
        szDataTemp = FileText
        #长度字符串缓存
        szLenTemp = ""
        #后续数据长度
        DataLen = 0
        #MD5
        szMD5 = ""
        
        #读取MD5数据长度
        szDataTemp = szDataTemp[2: ]
        szLenTemp = szDataTemp[0:3]
        DataLen = int(szLenTemp)
        if (32 != DataLen):
            logging.error("数据解密失败：MD5长度不正确")
            return 2
        #读取MD5
        szDataTemp = szDataTemp[3: ]
        szMD5 = szDataTemp[0:DataLen]
        #读取加密数据长度
        szDataTemp = szDataTemp[DataLen: ]
        szLenTemp = szDataTemp[0:3]
        DataLen = int(szLenTemp)
        
        #数据解密
        szDataTemp = szDataTemp[3: ]
        try:
            DecryptData = self._cDes.Decrypt(szDataTemp[0:DataLen], szMD5)
            if (None == DecryptData):
                logging.error("数据解密失败：导入的MD5值不正确")
                return 2
        except:
            logging.error("数据解密失败：未知原因")
            return 2
        
        #对解密后的数据进行分割
        Couple = DecryptData.split('-')
        if 6 > len(Couple):
            logging.error("数据解密失败：解密后的数据不符合要求")
            return 2
        self.UserName = Couple[0]
        self.Password = Couple[1]
        if '1' == Couple[2]:
            self.Dinner = True
        elif '0' == Couple[2]:
            self.Dinner = False
        else:
            return 3
    
        if '1' == Couple[3]:
            self.Bus = True
        elif '0' == Couple[3]:
            self.Bus = False
        else:
            return 3
        self.Reason = Couple[4]
        #验证用户名
        Md5Value = self.CalcMD5(self.UserName)
        if (Md5Value != szMD5):
            logging.error("数据解密失败：MD5值校验不通过")
            return 3
        
        #是否跳过登录
        if ('1' == Couple[5]):
            self.bSkip = True
    
        return 0
            
    #函数名称：CConfig::CheckUserPsw
    #函数功能：校验用户名和密码
    #函数返回：0正确 1参数错误 2网络错误 3用户名或密码错误
    #函数参数：UserName    :待验证的用户名
    #函数参数：Password    :待验证的密码
    def CheckUserPsw(self, UserName, Password):
        #HTTP会话类
        cHttp = CHttp()
        #登录成功定义
        SuccessStr = "正在进入OA系统，请稍候..."
        
        #验证数据有效性
        if (None==UserName or None==Password or ""==UserName or ""==Password):
            return 1
        
        #编码
        UserName = UserName.encode("GBK")
        Password = base64.b64encode(Password.encode("utf-8"))
        
        #登录的交互过程
        cHttp.Connect()
        ReqBody = urllib.parse.urlencode({'UNAME': UserName, 'PASSWORD': Password, 'encode_type': 1})
        if (False == cHttp.Send("POST", "/logincheck.php", ReqBody)):
            cHttp.Close()
            return 2
        AckCode, AckHead, AckBody = cHttp.Receive()
        if 200 != AckCode:
            cHttp.Close()
            return 2

        #验证登录结果
        Result = AckBody.find(SuccessStr)
        if -1 == Result:
            cHttp.Close()
            return 3
        cHttp.Close()
        
        return 0

                
#文件读写类
class CFileMng:
    __m_szPath = ""

    #函数名称：CFileMng::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：szFilePath：文件路径
    def __init__(self, szFilePath):
        self.__m_szPath = szFilePath


    #函数名称：CFileMng::ReadTextFile
    #函数功能：读取文本文件
    #函数返回：成功返回文件内容，失败返回None
    #函数参数：无
    def ReadTextFile(self):
        #打开文件
        try:
            File_Object = open(self.__m_szPath, 'r')
        except:
            return None

        #读取文件内容
        try:
            Text = File_Object.read()
        except:
            File_Object.close()

        File_Object.close()
        return Text


    #函数名称：CFileMng::WriteTextFile
    #函数功能：写入文本文件
    #函数返回：成功返回True,失败返回False
    #函数参数：szText    ：要写入的文本内容
    def WriteTextFile(self, szText):
        #打开文件
        try:
            File_Object = open(self.__m_szPath, 'w')
        except:
            return False

        #写入文件内容
        try:
            File_Object.write(szText)
        except:
            File_Object.close()

        File_Object.close()
        return True;


    #函数名称：CFileMng::DelTextFile
    #函数功能：删除文本文件
    #函数返回：无
    #函数参数：szFilePath：文件路径
    def DelTextFile(self):
        if False == os.path.exists(self.__m_szPath):
            return
        os.remove(self.__m_szPath)
        return