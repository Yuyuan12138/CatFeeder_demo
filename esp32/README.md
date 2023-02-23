## 喂猫机硬件代码设置

这一部分,我们最终实现的效果是,当摄像机拍下图片并在单片机上判断得出置信度后,我们会向事先搭建好服务器发送请求,服务器将返回值返给客户端进行阈值判断,得到`true`,即确认为猫后,我们的蜂鸣器,舵机,马达就会有条不紊地进行工作,将猫粮送出。

#### 硬件程序的编写的代码如下

```python
#在开始之前,我们要连接好相应的端口,引入相应的函数,以便后续调用
from machine import PWM,Pin#引入pwm,pin相关信息
import time#引入时间模块
from time import sleep_ms#从时间模块中引入延时函数sleep_ms(时间单位为毫秒)

beep = PWM(Pin(25),duty=0)#蜂鸣器接口为pin25,实现pwm脉冲调制,设置占空比为0
s1 = PWM(Pin(13),freq=50,duty=0)#在pin13处实现pwm脉冲调制,设置频率为50,占空比为0
p26 = PWM(Pin(26, Pin.OUT))#在pin26输出口处实现pwm脉冲调制

#我们第一步先来实现本地wifi的自动连接,方便猫脸检测过程中图片的上传
def do_connect(ssid,key):#定义自动连接wifi的函数,ssid是wifi名,key为wifi密码
    import network#引入micropython中的network库
    wlan = network.WLAN(network.STA_IF#客户端)#定义wlan
    wlan.active(True)#激活网络接口
    if not wlan.isconnected():
        print('connecting to network...')#若未联网则会显示正在连接...
        wlan.connect(ssid,key)#连接到无线网络
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())#返回4元组(ip,subnet,gateway,dns)
                        
#进行猫脸检测    
def test_cat()->bool:#定义猫脸检测的函数
    import urequests#引入urequest模块,以获取执行http post请求所需的函数
    res = urequests.post("http://www.baidu.com"#请求网站,parmas={"threshold":0.1},data=img)#利用post函数发送请求
    print(res.text#服务器响应内容的字符串形式)#获取请求的响应内容
    return True
          
#这里实现的效果是让蜂鸣器发声,暂停ms,再发出声音,暂停ms,循环n次,带入不同的n,ms,会发出不同的声音
def alarm(n,ms):#定义alarm函数让蜂鸣器有规律的发出声音
    beep.freq(500)#蜂鸣器的频率为500
    for i in range(n):
        beep.duty(10)
        sleep_ms(ms)
        beep.duty(0)
        sleep_ms(ms)
        
def Servo(servo,angle):#定义控制舵机旋转角度的servo函数
    servo.duty(int(((angle)/90+0.5)/20*1023)#占空比的计算公式)

def init():
    Servo(s1,90)#最初舵机设置为90度
    do_connect("TP-LINK_230B","ksam238267")#连接wifi
    
def motor_rotate():
    p26.freq(1000)#逆时针
    p26.duty(160)#设置p26的频率和占空比
    sleep_ms(3000)#延时3秒
    p26.deinit()
               
#确认为猫之后舵机,马达和蜂鸣器的一系列操作
def found_cat():
    Servo(s1,0)#舵机旋转为0度
    motor_rotate()#Todo:马达转3圈
    alarm(3,500)#蜂鸣器发声循环三次,暗示猫粮推出
    sleep_ms(2000)
    Servo(s1,90)#再调整为90度
    alarm(1,1000)#蜂鸣器发声循环一次,暗示恢复舵机恢复初始状态
#调用我们写好的函数的步骤
init()
test_cat()
sleep_ms(2000)#延时2000毫秒
found_cat()
```

这里我们这一段代码所实现的效果其实是,舵机初始设定为90度,当有猫出现时,我们会先自动连接网络,然后运行猫脸检测的函数`test_cat`,向网站发送请求,在得到网站的返回结果为true,识别为猫之后才会运行发现猫的函数`found_cat`,去驱动舵机旋转和马达转三圈以推出猫粮,在检测过程中,我们需要一段时间,所以设置了两秒的延时,再去运行`found_cat`
