import cve_glassfish_fileread
import cve_apache_ssi_rce

import index


def poc_fh():
    global n
    poc_start()
def glassfish_fileread_start():
    cve_glassfish_fileread.gf_start()
    poc_fh()



def poc_start():
    print('''
    #------漏洞利用------#
    \n1-GlassFish 任意文件读取漏洞\n2-Apache SSI 远程命令执行漏洞 
    ''')
    bianhao=input('[yzd@漏洞利用]#:')
    if bianhao=='back':
        index.back()

    if bianhao=='1':
        glassfish_fileread_start()
    if bianhao=='2':
        cve_apache_ssi_rce.apache_ssi()




if __name__ == '__main__':
    poc_start()