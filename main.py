import utime
from servo import Servo
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C



s1 = Servo(0)  # Servo pin is connected to GP0

sdaPin = Pin(16)
sclPin = Pin(17)
i2c = I2C(0, sda=sdaPin, scl=sclPin)
devices = i2c.scan()
oled = SSD1306_I2C(128, 64, i2c, addr=devices[0])


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

oled.fill(0)
oled.text("Tom's Hardware", 0, 0)
oled.show()