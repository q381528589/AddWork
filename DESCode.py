# -*- coding: utf-8 -*-

from DESStruct import *
from ConfigFileIO import *

__all__ = ['desencode']

class DES():
    def __init__(self):
        pass

    #加密
    def __Encode(self, from_code, key, code_len, key_len):
        output = ""
        trun_len = 0
        #将密文和密钥转换为二进制
        code_string = self.__functionCharToA(from_code, code_len)
        code_key = self.__functionCharToA(key, key_len)
        #如果密钥长度不是16的整数倍则以增加0的方式变为16的整数倍
        if code_len%16 != 0:
            real_len = (code_len/16) * 16 + 16
        else:
            real_len = code_len
        if key_len%16 != 0:
            key_len = (key_len/16) * 16 + 16
        key_len *= 4
        #每个16进制占4位
        trun_len = 4 * real_len
        #对每64位进行一次加密
        for i in range(0, trun_len, 64):
            run_code = code_string[i:i+64]
            l = i % key_len
            run_key = code_key[l:l+64]
            #64位明文、密钥初始置换
            run_code = self.__codefirstchange(run_code)
            run_key = self.__keyfirstchange(run_key)
            #16次迭代
            for j in range(16):
                #取出明文左右32位
                code_r = run_code[32:64]
                code_l = run_code[0:32]
                #64左右交换
                run_code = code_r
                #右边32位扩展置换
                code_r = self.__functionE(code_r)
                #获取本轮子密钥
                key_l = run_key[0:28]
                key_r = run_key[28:56]
                key_l = key_l[d[j]:28] + key_l[0:d[j]]
                key_r = key_r[d[j]:28] + key_r[0:d[j]]
                run_key = key_l + key_r
                key_y = self.__functionKeySecondChange(run_key)
                #异或
                code_r = self.__codeyihuo(code_r, key_y)
                #S盒代替/选择
                code_r = self.__functionS(code_r)
                #P转换
                code_r = self.__functionP(code_r)
                #异或
                code_r = self.__codeyihuo(code_l, code_r)
                run_code += code_r
            #32互换
            code_r = run_code[32:64]
            code_l = run_code[0:32]
            run_code = code_r + code_l
            #将二进制转换为16进制、逆初始置换
            output += self.__functionCodeChange(run_code, True)
        return output

    #解密
    def __Decode(self, string, key, key_len, string_len):
        output = ""
        trun_len = 0
        num = 0
        #将密文转换为二进制
        code_string = self.__functionCharToA(string, string_len)
        #获取字密钥
        code_key = self.__getkey(key, key_len)
        #如果密钥长度不是16的整数倍则以增加0的方式变为16的整数倍
        real_len = (key_len/16)+1 if key_len%16!=0 else key_len/16
        trun_len = string_len*4
        #对每64位进行一次加密
        for i in range(0, trun_len, 64):
            run_code = code_string[i:i+64]
            run_key = code_key[num % real_len]
            #64位明文初始置换
            run_code = self.__codefirstchange(run_code)
            #16次迭代
            for j in range(16):
                code_r = run_code[32:64]
                code_l = run_code[0:32]
                #64左右交换
                run_code = code_r
                #右边32位扩展置换
                code_r = self.__functionE(code_r)
                #获取本轮子密钥
                key_y = run_key[15-j]
                #异或
                code_r = self.__codeyihuo(code_r, key_y)
                #S盒代替/选择
                code_r = self.__functionS(code_r)
                #P转换
                code_r = self.__functionP(code_r)
                #异或
                code_r = self.__codeyihuo(code_l, code_r)
                run_code+=code_r
            num += 1
            #32互换
            code_r = run_code[32:64]
            code_l = run_code[0:32]
            run_code = code_r + code_l
            #将二进制转换为16进制、逆初始置换
            output += self.__functionCodeChange(run_code, False)
        return output

    #获取子密钥
    def __getkey(self, key, key_len):
        #将密钥转换为二进制
        code_key = self.__functionCharToA(key, key_len)
        a = [''] * 16
        real_len = (key_len/16)*16+16 if key_len%16!=0 else key_len
        b = [''] * (real_len/16)
        for i in range(real_len/16):
            b[i] = a[:]
        num = 0
        trun_len = 4 * key_len
        for i in range(0, trun_len, 64):
            run_key = code_key[i:i+64]
            run_key = self.__keyfirstchange(run_key)
            for j in range(16):
                key_l = run_key[0:28]
                key_r = run_key[28:56]
                key_l = key_l[d[j]:28] + key_l[0:d[j]]
                key_r = key_r[d[j]:28] + key_r[0:d[j]]
                run_key = key_l + key_r
                key_y = self.__functionKeySecondChange(run_key)
                b[num][j] = key_y[:]
            num += 1
        return b

    #异或
    def __codeyihuo(self, code, key):
        code_len = len(key)
        return_list = ''
        for i in range(code_len):
            if code[i] == key[i]:
                return_list += '0'
            else:
                return_list += '1'
        return return_list

    #密文或明文初始置换
    def __codefirstchange(self, code):
        changed_code = ''
        for i in range(64):
            changed_code += code[ip[i]-1]
        return changed_code

    #密钥初始置换
    def __keyfirstchange(self, key):
        changed_key = ''
        for i in range(56):
            changed_key += key[pc1[i]-1]
        return changed_key

    #逆初始置换
    def __functionCodeChange(self, code, bEncrypt):
        if bEncrypt:
            lens = len(code) / 4
        else:
            lens = 16
        return_list = ''
        for i in range(lens):
            list = ''
            for j in range(4):
                list += code[ip_1[i*4+j]-1]
            return_list += "%x" % int(list, 2)
        return return_list

    #扩展置换
    def __functionE(self, code):
        return_list = ''
        for i in range(48):
            return_list += code[e[i]-1]
        return return_list

    #置换P
    def __functionP(self, code):
        return_list = ''
        for i in range(32):
            return_list += code[p[i]-1]
        return return_list

    #S盒代替选择置换
    def __functionS(self, key):
        return_list = ''
        for i in range(8):
            row = int(str(key[i*6])+str(key[i*6+5]), 2)
            raw = int(str(key[i*6+1])+str(key[i*6+2])+str(key[i*6+3])+str(key[i*6+4]), 2)
            return_list += self.__functionTos(s[i][row][raw], 4)
        return return_list

    #密钥置换选择2
    def __functionKeySecondChange(self, key):
        return_list = ''
        for i in range(48):
            return_list += key[pc2[i]-1]
        return return_list

    #将十六进制转换为二进制字符串
    def __functionCharToA(self, code, lens):
        return_code = ''
        lens = lens % 16
        for key in code:
            code_ord = int(key,16)
            return_code += self.__functionTos(code_ord, 4)
        if lens != 0:
            return_code += '0' * (16-lens) * 4
        return return_code

    #二进制转换
    def __functionTos(self, o, lens):
        return_code = ''
        for i in range(lens):
            return_code = str(o>>i & 1) + return_code
        return return_code

    #将unicode字符转换为16进制
    def __tohex(self, string):
        return_string = ''
        for i in string:
            return_string += "%02x" % ord(i)
        return return_string

    def __tounicode(self, string):
        return_string = ''
        string_len = len(string)
        for i in range(0, string_len, 2):
            return_string += chr(int(string[i:i+2], 16))
        return return_string

    #DES加密
    def DESEncode(self, from_code, key):
        #转换为16进制
        from_code = self.__tohex(from_code)
        key = self.__tohex(key)
        des = DES()
        key_len = len(key)
        string_len = len(from_code)
        if string_len<1 or key_len<1:
            print 'error input'
            return False
        key_code = self.__Encode(from_code, key, string_len, key_len)
        return key_code

    #DES解密
    def DESDecode(self, from_code, key):
        key = self.__tohex(key)
        des = DES()
        key_len = len(key)
        string_len = len(from_code)
        if string_len%16 != 0:
            return False
        if string_len<1 or key_len<1:
            return False
        key_code= self.__Decode(from_code, key, key_len, string_len)
        return self.__tounicode(key_code)

#测试
if __name__ == '__main__':
    des = DES()
    print des.DESEncode('钱嘉欢-sh88861158-1-0-加班', '1024')
    print des.DESDecode('8f5ffb276d7f18241be565f22c48c83d2c4040432f3d9668e9834ee137b67156', '1024')
    # cFile = CFileMng(r'./AddWork.cfg')
    # if False == cFile.WriteTextFile("123456"):
    #     print("failed to write file")
    # else:
    #     print("success")