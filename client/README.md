## 喂猫机服务器代码设置

这一部分,我们最终实现的效果是,当摄像机拍下图片并在单片机上判断得出置信度后,我们会向事先搭建好服务器发送请求,服务器将返回值返给客户端进行阈值判断,得到`true`,即确认为猫后,我们的蜂鸣器,舵机,马达就会有条不紊地进行工作,将猫粮送出。



#### 服务器相关内容(主要是服务端的搭建以及客户端的接收)

这里我们首先搭建一个服务端

```python
#导入request库,json库,再从flask中导入Flask, session, make_response, redirect, url_for(路由指向函数)
import requests, json
from flask import Flask, session, make_response, redirect, url_for

app = Flask(__name__)#新建一个Flask可运行实体

@app.route('/', methods=['GET', 'POST']#支持请求的方法为POST,GET,默认为get) #定义一个本地路由
def data_handler() :
   
    #路径定义，方便单片机B接收
    r = make_response('<p>Accomplished</p>')
    r.set_cookie('confidence', str(traceback))
    return r
    #利用make_response函数自定义自己的response,当服务器接收到变量后,会返回一个accomplished的页面,名称为confidence,内容是字符串形式的traceback
           
with open('web/jpg/1.jpg', 'rb') as f:#以二进制只读模式打开名为'web/jpg/1.jpg'的文件
    img = f.read()#读取图片
#向识别服务器提交请求
result = requests.post('http://127.0.0.1:24401/', params={'threshold': 0.1},
                                                  data=img).json()#以json字典格式向网站发送请求,传递参数

global traceback
# 全局化,方便后续引用
traceback = result["results"][0]["confidence"]
#变量赋值,取出result中第一个变量的置信度           

app.run(port= , debug=True#设置DEBUG模式参数,开启调试模式)#运行Flash实体
#port端口号 默认于127.0.0.1运行
```

在这个过程中,我们首先建立一个`flask`框架,后续代码都是在这个框架下运行,定义一个本地路由,包括`data_handler`函数,这样基础就完成了,当我们打开文件读取其中的内容,向网站发送请求时,网站就会运行我们已经定义好的`datahandler`函数,显示出置信度的页面。



下面,我们模拟客户端并获取服务端`confidence(Cookie)`的值

```python
#引入需要的库
import threading
import urllib.request, requests

handler_url = 'http://......'#对本地服务器进行连接并赋值给handler_url
#此处为main.py中的ip地址+main.py中/data/api/handle路径
confidence ='Null'
class check_data(threading.Thread) :#定义类(线程)
        def __init__(self, confidence) :#初始化函数
                threading.Thread.__init__(self)
                self.confidence = confidence
                self.stopped = False#状态设置为一直进行

        def run(self) :
                global handler_url#对url进行全局化设置


                while not self.stopped :
                        try :
                       
                                r = requests.get(handler_url)
                                Specimen = r.cookies['confidence']
                                print(Specimen)#如果self.stopped为true,则向网站发送请求,并打印出cookie值
                        except KeyError:
                                pass
                        self.stopped = self.stopped or self.confidence == Specimen 
#若self.stopped:true,或者获取到了cookie值,就会暂停1.5秒
                        self.event.sleep(1.5)
             
```

在这一段代码中,我们主要进行两步,初始化参数和获取`cookie`值,确保客户端可以正常接收到返回值即可
