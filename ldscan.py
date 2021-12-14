import socket
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def SQL():
    i=1
    url=input('please enter url:\n')
    ii=len(url)
    while i<ii:
        str1=url[i]
        str2=url[i+1]
        if str1=='?':
            no1 = url.find(str1, 0, ii)
        if str2=='=':
            no2 = url.find(str2, 0, ii)
        cs=url[str1:str2]
        print(cs)
        i=i+1













if __name__ == '__main__':
    print('''
    1-SQLscan
    ''')
    s=input(':')
    SQL()
