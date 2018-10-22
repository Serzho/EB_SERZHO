#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import edubot #подлючение модулей
from time import sleep
from xmlrpc.server import SimpleXMLRPCServer
import threading

from ina219 import INA219
from ina219 import DeviceRangeError
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import example

IP = '192.168.8.160'
PORT = 8000

servoPos = 62

#поток для контроля напряжения и тока
#параметр
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time


class StateThread(threading.Thread):
    
    def __init__(self, robot):
        super(StateThread, self).__init__()
        self.daemon = True
        self._stopped = threading.Event() #событие для остановки потока
        self._robot = robot
        
    def run(self):
        print('State thread started')
        while not self._stopped.is_set():
            
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            draw.text((0, 0), "GOSPOD BOH SERZHO", font=font, fill=255)
            draw.text((0, 8), "Voltage: %.2f" % ina.voltage(), font=font, fill=255)
            draw.text((0, 16), "Current: %.2f" % ina.current(), font=font, fill=255)
            draw.text((0, 24), "Power: %.2f" % ina.power(), font=font, fill=255)
            
            disp.image(image)
            
            disp.display()
            
            sleep(1)
            
        print('State thread stopped')

def stop(self): #остановка потока
        self._stopped.set()
        self.join()

def Speak():
    # бибикнуть
    robot.Beep()
    return 0

def SetSpeed(leftSpeed, rightSpeed):
    robot.leftMotor.SetSpeed(leftSpeed)
    robot.rightMotor.SetSpeed(rightSpeed)
    return 0

def StopMotor():    
    robot.leftMotor.SetSpeed(0)
    robot.rightMotor.SetSpeed(0)
    return 0

def ServoUp():
    global servoPos
    servoPos -= 10
    if servoPos < 0:
        servoPos = 0
    robot.servo[0].SetPosition(servoPos)
    print ('ServoPos = %d' % servoPos)
    return 0

def ServoDown():
    global servoPos
    servoPos += 10
    if servoPos > 125:
        servoPos = 125
    robot.servo[0].SetPosition(servoPos)
    print ('ServoPos = %d' % servoPos)
    return 0

SHUNT_OHMS = 0.01
MAX_EXPECTED_AMPS = 2.0

ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

robot = edubot.EduBot(1)
assert robot.Check(), 'EduBot not found!!!'
print ('EduBot started!!!')

#128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst = None)

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
disp.clear()

# Load default font.
font = ImageFont.load_default()

stateThread = StateThread(robot)
stateThread.start()


# Создаем сервер (IP адрес, порт, отключен лог)
server = SimpleXMLRPCServer((IP, PORT), logRequests = False)
print('Control XML-RPC server listening on %s:%d' % (IP, PORT))

# регистрируем функции
server.register_function(Speak)
server.register_function(SetSpeed)
server.register_function(StopMotor)
server.register_function(ServoUp)
server.register_function(ServoDown)

# запускаем сервер
try:
    robot.Start()
    server.serve_forever()
    example.run()
except KeyboardInterrupt:
    robot.servo[0].SetPosition(62)
    robot.leftMotor.SetSpeed(0)
    robot.rightMotor.SetSpeed(0)
    robot.Release()
    stateThread.stop()
    disp.clear()
    disp.display()
    print('Stop program')
