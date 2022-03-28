from time import sleep
from machine import Pin, PWM
import network
from network import WLAN
from mqtt import MQTTClient
def sub_callback(topic, msg): 
    if topic.decode("utf-8")=="espriella/feeds/servoduty":
        servo.duty(int(msg))
        sleep(2)
        servo.duty(0)
    print(topic, msg)
def settimeout(duration): 
    pass

wlan = WLAN(network.STA_IF)
if not wlan.isconnected():
    wlan.active(True)
    wlan.connect("hydra", "**************")
    while not wlan.isconnected(): 
        pass
print("Connected to Wifi", wlan.ifconfig())

client = MQTTClient("LOLIN32", "io.adafruit.com",user="espriella", password="*******************", port=1883)
client.settimeout = settimeout
client.set_callback(sub_callback)
client.connect()
client.subscribe(topic="espriella/feeds/servoduty")
servo = PWM(Pin(23))
servo.freq(50)
while True:
    client.check_msg()
