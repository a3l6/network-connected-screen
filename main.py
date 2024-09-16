import network
import utime
from servo import Servo
import time
from machine import Pin, I2C, reset
from ssd1306 import SSD1306_I2C
from umqtt import MQTTClient
import network
import secrets



s1 = Servo(0)  # Servo pin is connected to GP0

sdaPin = Pin(16)
sclPin = Pin(17)
i2c = I2C(0, sda=sdaPin, scl=sclPin)
devices = i2c.scan()
#time.sleep(5)
if devices == []:
    reset()
oled = SSD1306_I2C(128, 64, i2c)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PASSWORD)
time.sleep(5)
print(wlan.isconnected())

mqtt_server = "broker.hivemq.com"
client_id = "a3l6"
topic_sub = b"Toggle"


def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=7200)
    client.set_callback(subscribe)
    client.connect()


    print(f"Connected to {mqtt_server} MQTT Broker")
    return client

def reconnect():
    print("Failed to connect to the MQTT Broker. Reconnecting...")
    time.sleep(5)
    reset()

def subscribe(topic, msg):
    print(f"New message on topic {topic.decode('utf-8')}")
    msg = msg.decode('utf-8')
    print(msg)

    if msg == "on":
        print("ON")
    else:
        print("OFF")

try:
    client = mqtt_connect()
except OSError:
    reconnect()

while True:
    client.subscribe(topic_sub)
    time.sleep(1)

def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle, 0, 180, 0, 1024)))  # Convert range value to angle value


def left():
    for i in range(0, 180, 10):
        servo_Angle(i)



def right():
    for i in range(180, 0, -10):
        servo_Angle(i)
        utime.sleep(0.05)

#oled.fill(0)
#oled.text("Tom's Hardware", 0, 0)
#oled.show()