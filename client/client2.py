import threading
import urllib.request, requests
handler_url = 'http://127.0.0.1:24402'
#此处为main.py中的ip地址+main.py中/data/api/handle路径
confidence = 'Null'
#定义类（线程）
class check_data(threading.Thread) :
        #初始化线程
        def __init__(self, confidence) :
                threading.Thread.__init__(self)
                self.event = threading.Event()
                self.confidence = confidence
                #线程终止（default:False)
                self.stopped = False
        #定义全局变量的函数

        def run(self) :
                global handler_url
                global Specimen
                #循环（条件：self.stopped:False)
                while not self.stopped :
                        #捕获异常
                        try :
                                #获取ip地址
                                r = requests.get(handler_url)
                                #获取cookie
                                Specimen = r.cookies['confidence']
                                #print
                                print(Specimen)
                                f = open("C:/Users/13595/Desktop/get_confidence.txt", "w")
                                f.write(str(Specimen))
                                f.close()
                        #未存在cookie
                        except KeyError:
                                pass
                        #停止条件self.stopped:True或获取到了存在的cookie值
                        self.stopped = self.stopped or self.confidence == Specimen
                        #间隔1.5秒再次获取cookie
                        self.event.wait(1.5)
c = check_data(confidence)
c.start()
#
#
#
#


