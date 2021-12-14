import xxsj
import fuzz
import xxsj_nw
import poc
import queue
q=queue.Queue()

def back():
    index_start()
def index_start():
    print('''
                                                     $$\ 
                                                     $$ |
               $$\   $$\       $$$$$$$$\        $$$$$$$ |
               $$ |  $$ |      \____$$  |      $$  __$$ |
               $$ |  $$ |        $$$$ _/       $$ /  $$ |
               $$ |  $$ |       $$  _/         $$ |  $$ |
               \$$$x$$$ |      $$$$y$$$\       \$$$m$$$ |
                \____$$ |      \________|       \_______|
               $$\   $$ |                                
               \$$$$$$  |                                
                \______/                                 
                   ''')
    print('1-信息搜集\n2-爆破\n3-内网信息搜集\n4-漏洞利用\n5-getshell')
    canshu = input('#:')
    if canshu=='1':
        xinxisouji()
    else:
        if canshu=='2':
            baopo()
        else:
            if canshu=='3':
                xinxisouji_nw()
            else:
                if canshu=='4':
                    loudongliyong()



def xinxisouji():
    xxsj.start()
def baopo():
    fuzz.start()
def xinxisouji_nw():
    xxsj_nw.start()
def loudongliyong():
    poc.poc_start()





if __name__ == '__main__':
    index_start()







