import nmap
nm = nmap.PortScanner()
import os
import threading
import index
import re




#起始
def start():
    print('''
     #------内网信息搜集------#
    \n1-存活主机扫描\n2-查看系统信息\n3-查看网络信息\n4-查看服务信息\n5-查看计划任务\n6-设置防火墙功能
    ''')
    cs=input('[yzd@内网信息收集]#:')
    if cs=='1':
        ips = input('网段:')
        ips = ips.split('.')
        ip = ips[0] + '.' + ips[1] + '.' + ips[2] + '.'
        port=input('范围:')
        port = port.split('-')
        p1 = int(port[0])
        p2 = int(port[1])
        p = int(p2) - int(p1) + 1
        xcs = int(input('线程数:'))
        a = p // xcs
        while p % xcs != 0:
            xcs = xcs + 1
        d = dxc(cs)
        d.build(xcs, a, ip, p1)
    if cs=='2':
        sysinfo()
    if cs=='3':
        netinfo()
    if cs=='4':
        service()
    if cs=='5':
        plan()
    if cs=='6':
        fire().xg()
    if cs=='back':
        index.back()

#   多线程
class dxc():
    def __init__(self,cs):
        self.cs=cs
    def build(self,xcs,a,ip,p1):
        n=1
        while n<=xcs:
            t=threading.Thread(target=ipscan(ip,p1,a,n))
            t.start()
            n+=1
#存活主机扫描
def ipscan(ip,p1,a,n):
    a=int(a)
    if n==1:
        while p1<=n*a:
            cmd = 'ping '+ip+str(p1)+' -n 2'
            try:
                data = os.popen(cmd).read()
                ttl=data.find('TTL',0,len(data))
                if ttl!=-1:
                    print('[+] '+ip+str(p1))
            except EOFError as e:
                print('[-] 执行出错')
            p1+=1
    if n!=1:
        p1=n*a-1
        while p1<=n*a:
            cmd = 'ping '+ip+str(p1)+' -n 2'
            try:
                data = os.popen(cmd).read()
                ttl = data.find('TTL', 0, len(data))
                if ttl != -1:
                    print('[+] ' + ip + str(p1))
            except EOFError as e:
                print('[-] 执行出错')
            p1+=1

#查看当前主机系统信息
def sysinfo():
    data=os.popen('systeminfo').read()
    data_cd=len(data)

    #系统基本信息
    zhu1=data.find('主',0,data_cd)
    zhu2=data.find('注',0,data_cd)
    zhu2=zhu2-1
    zhu=data[zhu1:zhu2]
    print('\n######系统基本信息:\n'+zhu)
    
    #处理器信息
    chu=data.find('处',0,data_cd)
    qu=data.find('区',0,data_cd)
    qu=qu-2
    c=data[chu:qu]
    print(c+'\n')

    #补丁信息
    xiu=data.find('修',0,data_cd)
    ka=data.find('卡',0,data_cd)
    ka=ka-1
    kb=data[xiu:ka]
    an=kb.find('安',0,len(kb))
    kb=kb[an:ka]
    kb=kb.replace(' ','')
    print('######补丁信息:\n'+kb+'\n')


    #域信息
    ye=data.find('页',0,data_cd)
    yu_data=data[ye:xiu]
    yu=yu_data.find('域',0,len(yu_data))
    yu_data=yu_data[yu:xiu]
    yu_data.replace(' ','')
    yu_data.replace('\n','')

    #用户信息
    yh_data = os.popen('net user').read()
    yh_cd=len(yh_data)
    zhang = yh_data.find('帐', 0, yh_cd)
    zhang=zhang+2
    ming=yh_data.find('命',0,yh_cd)
    yh_data = yh_data[zhang:ming]
    yh_data=yh_data.replace('-','')
    yh_data = yh_data.replace('\n', '')
    print('###用户信息:\n'+yu_data+'用户名:      '+yh_data)
    #当前用户权限
    yh_qx = str(os.popen('whoami').read().encode('utf-8'))
    print('当前用户权限: '+yh_qx)
#查看当前主机网络信息
def netinfo():
    net_data = os.popen('ipconfig /all').read()
    print(net_data)

#服务信息
def service():
    service_data=str(os.popen('wmic service list brief').read())
    print(service_data)
#计划任务
def plan():
    plan_data=str(os.popen('schtasks /query /fo LIST /v').read())
    print(plan_data)
#设置防火墙
class fire():
    def mz(self):
        cxm = input('程序名:')
        lj = input('程序位置:')
        cl=cxm+'|'+lj
        return cl
    def xg(self):
        select=input('1-允许指定程序进入\n2-允许指定程序退出\n3-关闭防火墙\n#:')
        cl=fire().mz().split("|")
        if select=='1':
            fhz=str(os.popen('netsh advfirewall firewall add rule name='+'"'+cl[0]+'"'+' dir=in action=allow program='+'"'+cl[1]+'" enable=yes'))
            print(fhz)
        if select=='2':
            fhz=str(os.popen('netsh advfirewall firewall add rule name='+'"'+cl[0]+'"'+' dir=out action=allow program='+'"'+cl[1]+'" enable=yes'))
            print(fhz)
        if select=='3':
            fhz = str(os.popen('netsh firewall set opmode disable'))
            print(fhz)












if __name__ == '__main__':
    start()





