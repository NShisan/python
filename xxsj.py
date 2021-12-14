#encoding=utf-8
import socket
import re
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
import whois
import time
import base64
from lxml import etree
import requests
import threading
import queue
q=queue.Queue()
import index
import nmap
nm=nmap.PortScanner()



#起始
class inputhost():
    def input_host(self):
        host=input('host:')
        if host=='back':
            fh()
        return host
    def conversion(self):
        host=input('ip/host:')
        if host=='back':
            fh()
        ip = socket.gethostbyname(host)
        print('\n' + 'IP: ' + ip + '\n')
        return ip
def start():
    print('''
    #------[信息搜集]------#
    ''')
    global cs
    cs = input('1-端口扫描(默认扫描所有端口)\n2-常用端口扫描\n3-whois查询\n4-子域名查询\n5-fofa搜索\n6-后台扫描\n[yzd@信息收集]#:')

    if cs=='fofa' or cs=='5':
        fofa()
    else:
        if cs=='back':
            index.back()
        else:
            if cs == '1':
                build_port()
            if cs == '2':
                ports_scan()
            if cs == '3':
                whois_check()
            if cs == '4':
                zym_check()
            if cs=='6':
                print('url格式(http://xxx.com/ 或 https://xxx.com/)')
                dirscan()

def fh():
    start()




#判断扫描的端口是否开放
def pd(result,p):
    if result == 0:
        print('\n' + str(p) + '-open!' + '\n' + '！！！！！！！###[end]###！！！！！！')


#全端口扫描
def allport_scan(n,a,ip):
    if n == 1:
        p = 1
        while p <= n * a:
            try:
                result = server.connect_ex((ip, p))
                pd(result, p)
                p = p + 1
            except Exception as a:
                print('error\n' + a)
    else:
        p = a * (n - 1) + 1
        while p <= n * a:
            try:
                result = server.connect_ex((ip, p))
                pd(result, p)
                p += 1
            except Exception as a:
                print('error\n' + a)
    fh()



#常用端口扫描
def ports_scan():
    i=inputhost()
    ip=i.conversion()
    ports = {'21', '23', '25', '53', '69', '80', '135', '137', '139', '443', '1080', '1521', '1433', '3306', '3389'}
    for port in ports:
        try:
            result = server.connect_ex((ip, int(port)))
            pd(result, port)
        except Exception as a:
            print('error\n'+a)
    fh()

#创建多线程-----端口扫描
def build_port():
    i=inputhost()
    ip = i.conversion()
    dk=input('1-65535')
    if dk=='':
        ports = 65535  # 端口数
        xcs = 520  # 线程数
        a = ports // xcs  # 每个线程分配端口
        while ports % xcs != 0:
            xcs = xcs + 1  # 添加一个线程扫描多余端口
        n = 1  # 控制线程数量
        while n <= xcs:
            t = threading.Thread(target=allport_scan(n,a,ip))
            t.start()
            n = n + 1
    else:
        dk=dk.split('-')
        sp=dk[0]
        ep=dk[1]
        ports=int(ep)-int(sp)+1
        xcs=int(input('线程数:'))
        a=ports//xcs
        while ports % xcs != 0:
            xcs = xcs + 1  # 添加一个线程扫描多余端口
        n = 1  # 控制线程数量
        while n <= xcs:
            t = threading.Thread(target=allport_scan(n, a,ip))
            t.start()
            n = n + 1
    fh()

#二、whois查询
def whois_check():
    i=inputhost()
    url=i.input_host()
    data=whois.whois(url)
    print('The obtained whois information is：\n' + str(data) + '\n！！！！！！！###[end]###！！！！！！')
    with open(r'whois.txt', 'a+') as f:
        f.write(str(data))
        f.close()
    fh()

#三、子域名查询
def zym_check():
    dic_load(cs)
    while not q.empty():
        zym_urls=q.get()
        try:  # ---异常处理
            zym_ip = socket.gethostbyname(zym_urls)  # ---ping子域名来检测是否存在
            print('正在运行。。。。。。\n[+]已经扫描到如下结果\n'+zym_urls + '-->' + zym_ip)
            time.sleep(0.1)
            with open(r'zym_result.txt', 'a+') as f:
                f.write(zym_urls+'-->'+zym_ip+ '\n')
                f.close()
        except Exception as e:
            # print('执行出错')
            pass
    fh()
#fofa搜索:https://fofa.so/result?qbase64=YQ%3D%3D
def fofa():
    cookie='Hm_lvt_b5514a35664fd4ac6a893a1e56956c97=1638002505,1638002550; Hm_lpvt_b5514a35664fd4ac6a893a1e56956c97=1638002566; befor_router=%2Fresult%3Fqbase64%3DYXBhY2hl; fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTI3MTAyLCJtaWQiOjEwMDA3NTY1NSwidXNlcm5hbWUiOiLniZvljYHkuIkiLCJleHAiOjE2MzgwNDU3NDh9.XwvEewtg4FIXgTm2D3eWI3ubMSzFuIhB11CcAo3tLGe3R6Rt3-lKCSDB_ilYjF_2wp1nqlQqyTYTt8wncmH_pw; user=%7B%22id%22%3A127102%2C%22mid%…level%22%3A0%2C%22company_name%22%3A%22%E7%89%9B%E5%8D%81%E4%B8%89%22%2C%22coins%22%3A0%2C%22credits%22%3A23%2C%22expiration%22%3A%22-%22%2C%22login_at%22%3A1638002548%7D; refresh_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTI3MTAyLCJtaWQiOjEwMDA3NTY1NSwidXNlcm5hbWUiOiLniZvljYHkuIkiLCJleHAiOjE2MzgyNjE3NDgsImlzcyI6InJlZnJlc2gifQ.TdEh8dv8PJUtUW0SsZr7CyoZiKcXlITfVGu_GBMuOQ_7zArV2pTk2u-Ot0fl-95W3M8MhrxqFilFcvv08eQo9Q'
    key = input('search:')
    fofa_url = 'https://fofa.so/result?qbase64='
    key = str(base64.b64encode(key.encode('utf-8')), 'utf-8')
    print(key)
    for yeshu in range(1, 6):
        print('正在导出第' + str(yeshu) + '页')
        search_url = fofa_url + key + '&page=' + str(yeshu) + '&page_size=10'
        try:
            result = requests.get(url=search_url).content
            soup = etree.HTML(result)
            ip_data = soup.xpath('//a[@target="_blank"]/@href')
            print('result:')
            print(ip_data)
            ip_data = '\n'.join(ip_data)
            with open(r'result/fofa_result.txt', 'a+') as f:
                f.write(ip_data + '\n')
                f.close()
        except Exception as e:
            time.sleep(0.5)
            pass
    fh()

#目录扫描------
def dirscan():
    dic_load(cs)
    while not q.empty():
        dir_urls=q.get()
        try:  # ---异常处理
            data=requests.get(dir_urls)
            if data.status_code==200:
                print('[+]已经扫描到如下结果\n'+dir_urls)
                time.sleep(0.1)
                with open(r'dir.txt', 'a+') as f:
                    f.write(dir_urls+ '\n')
                    f.close()
        except Exception as e:
            # print('执行出错')
            pass



#字典加载
class default_dic():
    def __init__(self, canshu):
        self.cs = canshu
        self.zt = ''
        if cs == '4':
            self.zt = 'zym'
        if cs == '6':
            self.zt = 'dir'
    def file_dic(self):
        file='dic/'+self.zt+'.txt'
        return file
def dic_load(cs):
    canshu=cs
    d = default_dic(canshu)
    i=inputhost()
    url=i.input_host()
    select_dic=input('1-默认字典\n2-导入字典\n#:')
    if cs=='4':
        url = url.replace('www.', '')
        if select_dic=='1':
           f=d.file_dic()
           print(f)
           for zym_data in open(f):
               zym_data = zym_data.replace('\n', '')  # ---屏蔽换行符
               urls = zym_data + '.' + url
               q.put(urls)
        if select_dic=='2':
            zym_file = input('导入字典：')
            for zym_data in open(zym_file):
                zym_data = zym_data.replace('\n', '')  # ---屏蔽换行符
                urls = zym_data + '.' + url
                q.put(urls)
    if cs=='6':
        dir_url=url
        while dir_url[0:4]!='http' or dir_url[-1]!='/':
            dir_url = input('url格式不对(http://xxx.com/ 或 https://xxx.com/):')
        else:
            if select_dic == '1':
                f=d.file_dic()
                print(f)
                for dir in open(f):
                    dir = dir.replace('\n', '')  # ---屏蔽换行符
                    urls = dir_url + dir
                    q.put(urls)
            if select_dic == '2':
                dir_file = input('导入字典：')
                for dir in open(dir_file):
                    dir = dir.replace('\n', '')  # ---屏蔽换行符
                    urls = dir_url+dir
                    q.put(urls)

if __name__ == '__main__':
    start()




























