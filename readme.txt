运行环境要求：
1.目前已知该版本在Windows7/8/10 64位系统上可以运行。
2.可能需要安装Microsoft Visual C++ 2015,需要安装的软件包已上传至Publisher。
3.AddWork.exe和update.exe必不可少；version.txt必须存在。否则可能会导致更新程序无法正常运行。

编译环境要求：
1.编译所需python环境：Python3.x。
2.编译所需的pyqt环境：PyQt5以上，安装命令：pip install pyqt5。
2.ui文件建议使用QT Designer编辑。
3.编译成exe建议使用pyinstaller 3.3以上的版本。

常用命令：
UI文件转py文件：pyuic5 -o xxx.py xxx.ui
编译主程序命令:
	pyinstaller -p "D:\Program Files\Python36\Lib\site-packages\PyQt5\Qt\bin" --version-file="./Version_Info.txt" -w -F Main.py
	找到相对目录下的/dist文件夹，重命名Main.exe文件：rename Main.exe AddWork.exe
编译更新程序命令：
	pyinstaller -p "D:\Program Files\Python36\Lib\site-packages\PyQt5\Qt\bin" -w -F update.py

已知bug：
1.用户从未登录时，默认密码为“synwa@2171”,登录后网页自动跳转，此时可能会因为pcre匹配不通过而显示用户名或密码错误。
2.修改密码没有抓取到数据包，目前没有相应的代码。

后期可能添加：
1.修改密码功能。
2.自动更新多线程断点下载。
3.主程序检测今日是否报名加班。
4.主程序右上角添加设置模块。