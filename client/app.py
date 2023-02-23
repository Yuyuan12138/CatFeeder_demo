import requests, json
from flask import Flask, session, make_response, redirect, url_for, request



#实例化FLASK模块
app = Flask(__name__)



@app.route('/', methods=['GET', 'POST']) 
#定义函数方便其他路由进行跳转
def data_handler() :
   
    #f命名为图像文件
    with open("C:/Users/13595/Desktop/cat_4.jpg", 'rb') as f:
#图像读取
        img = f.read()
#图片上传AISTUDIO本地sdk服务器，并转化为python字典形式
    result = requests.post('http://127.0.0.1:24401/', params={'threshold': 0.1},
                                                  data=img).json()
#全局变量traceback
    global traceback

#traceback为返回字典results键键值中正序第一项即置信度的值
    traceback = result["results"][0]["confidence"]
    print(traceback)

    r = make_response()
#将置信度传递至浏览器cookie中
    r.set_cookie('confidence', str(traceback))
    e = request.cookies.get('confidence')
    print(e)
    return r

app.run(port=24402, debug=True)
#port端口号 默认于127.0.0.1运行，host设置ip进行运行（default:   127.0.0.1:80)