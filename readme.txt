环境要求：
1.编译所需环境：PyQt5, Python3.x。
2.ui文件建议使用QT Designer编辑。
3.编译成exe建议使用pyinstaller 3.3以上的版本。

常用命令：
UI文件转py文件：pyuic5 -o xxx.py xxx.ui
打包命令:pyinstaller -p "D:\Program Files\Python36\Lib\site-packages\PyQt5\Qt\bin" -w -F Main.py

已知bug：
1.用户从未登录时，默认密码为“synwa@2171”,登录后网页自动跳转，此时可能会因为pcre匹配不通过而显示用户名或密码错误。
2.修改密码没有抓取到数据包，目前没有相应的代码。

后期准备增加：
1.自动检测更新功能。
2.修改密码功能。

联系方式：
1.如遇到问题，请联系网络事业部-钱嘉欢童鞋。