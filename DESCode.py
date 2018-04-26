# -*- coding: utf-8 -*-

from pyDes import *
import binascii
from binascii import unhexlify as unhex

class CDESCode:
    #函数名称：CDESCode::__init__
    #函数功能：构造函数
    #函数返回：无
    #函数参数：无
    def __init__(self):
        pass

    #函数名称：CDESCode::Encrypt
    #函数功能：3DES加密
    #函数返回：正确返回加密后的字符串，失败返回None
    #函数参数：Data       ：原始数据
    #函数参数：UserMD5    ：用户名的MD5
    def Encrypt(self, Data, UserMD5):
        #检验数据有效性
        if (32 != len(UserMD5)):
            return None
        #转为大写
        UserMD5 = UserMD5.upper()
        
        #转成utf-8格式
        Data = Data.encode("utf-8")
        #补齐至8的整数倍
        FillingLen = (8 - (len(Data)%8)) % 8
        for i in range(0, FillingLen, 1):
            Data += b'\0'
        #计算key
        key1 = des(unhex(UserMD5[0:16]))
        key2 = des(unhex(UserMD5[16:32]))
        key3 = des(unhex("0F1E2D3C4B5A6978"))
        #3次加密计算
        e1 = key1.encrypt(Data)
        e2 = key2.decrypt(e1)
        e3 = key3.encrypt(e2)
        #结果转为16进制字符串
        return binascii.b2a_hex(e3)

    #函数名称：CDESCode::Decrypt
    #函数功能：3DES解密
    #函数返回：正确返回加密后的字符串，失败返回None
    #函数参数：EncData    ：原始数据
    #函数参数：UserMD5    ：用户名的MD5    
    def Decrypt(self, EncData, UserMD5):
        #查找'\0'的索引值
        Index = 0
        #解密后的数据
        DecData = ""
        
        #检验数据有效性
        if (32 != len(UserMD5)):
            return None
        #转为大写
        UserMD5 = UserMD5.upper()
        
        #转成二进制串
        EncData = binascii.a2b_hex(EncData)
        #计算key
        key1 = des(unhex(UserMD5[0:16]))
        key2 = des(unhex(UserMD5[16:32]))
        key3 = des(unhex("0F1E2D3C4B5A6978"))
        #3次解密计算
        d3 = key3.decrypt(EncData)
        d2 = key2.encrypt(d3)
        d1 = key1.decrypt(d2)
        
        #去除多余的'\0'
        d1 = d1.decode("utf-8")
        for Index in range (0, len(d1), 1):
            if ('\0' == d1[Index]):
                DecData = d1[0:Index]
                break
        #没有多余的'\0'
        if (Index == len(d1)-1):
            DecData = d1
        
        return DecData