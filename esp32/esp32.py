from machine import PWM, Pin
import time
from time import sleep_ms

beep = PWM(Pin(25), duty=0)
s1 = PWM(Pin(13), freq=50, duty=0)
p26 = PWM(Pin( 26, Pin.OUT))  # 新加的部分

f = open("get_confidence1.txt", "r")
a = float(f.readline())


# def do_connect(ssid,key):
#     import network
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     if not wlan.isconnected():
#         print('connecting to network...')
#         wlan.connect(ssid,key)
#         while not wlan.isconnected():
#             pass
#     print('network config:', wlan.ifconfig())
#
# def test_cat()->bool:
#     import urequests
#     res = urequests.post("http://127.0.0.1:24403/",parmas={"threshold":0.1},data=img)
#     print(res.text)
#     return True

def alarm(n, ms):
    beep.freq(500)
    for i in range(n):
        beep.duty(10)
        sleep_ms(ms)
        beep.duty(0)
        sleep_ms(ms)


def Servo(servo, angle):
    servo.duty(int(((angle) / 90 + 0.5) / 20 * 1023))


# def init():
#     Servo(s1,90)
#     do_connect("TP-LINK_3A12","13770449798")

def motor_rotate():
    p26.freq(1000)  # 逆时针
    p26.duty(160)
    sleep_ms(3000)
    p26.deinit()


def found_cat():
    Servo(s1, 0)
    motor_rotate()  # Todo:马达转3圈
    alarm(3, 500)
    sleep_ms(5000)
    Servo(s1, 90)
    sleep_ms(1000)
    alarm(1, 1000)

if a>0.5:
    found_cat()
f.close()
