���л���Ҫ��
1.Ŀǰ��֪�ð汾��Windows7/8/10 64λϵͳ�Ͽ������С�
2.������Ҫ��װMicrosoft Visual C++ 2015,��Ҫ��װ����������ϴ���Publisher��
3.AddWork.exe��update.exe�ز����٣�version.txt������ڡ�������ܻᵼ�¸��³����޷��������С�

���뻷��Ҫ��
1.��������python������Python3.x��
2.���������pyqt������PyQt5���ϣ���װ���pip install pyqt5��
2.ui�ļ�����ʹ��QT Designer�༭��
3.�����exe����ʹ��pyinstaller 3.3���ϵİ汾��

�������
UI�ļ�תpy�ļ���pyuic5 -o xxx.py xxx.ui
��������������:
	pyinstaller -p "D:\Program Files\Python36\Lib\site-packages\PyQt5\Qt\bin" --version-file="./Version_Info.txt" -w -F Main.py
	�ҵ����Ŀ¼�µ�/dist�ļ��У�������Main.exe�ļ���rename Main.exe AddWork.exe
������³������
	pyinstaller -p "D:\Program Files\Python36\Lib\site-packages\PyQt5\Qt\bin" -w -F update.py

��֪bug��
1.�û���δ��¼ʱ��Ĭ������Ϊ��synwa@2171��,��¼����ҳ�Զ���ת����ʱ���ܻ���Ϊpcreƥ�䲻ͨ������ʾ�û������������
2.�޸�����û��ץȡ�����ݰ���Ŀǰû����Ӧ�Ĵ��롣

���ڿ�����ӣ�
1.�޸����빦�ܡ�
2.�Զ����¶��̶߳ϵ����ء�
3.������������Ƿ����Ӱࡣ
4.���������Ͻ��������ģ�顣