# -*- coding: utf-8 -*-

import os

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