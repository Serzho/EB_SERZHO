#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import edubot

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

#128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst = None)

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
robot = edubot.EduBot(1)

draw = ImageDraw.Draw(image)

# Clear display.
disp.clear()

# Load default font.
font = ImageFont.load_default()

assert robot.Check(), 'EduBot not found!!!'

robot.Start()
print('EduBot started!!!')

robot.Beep()

try:
    #robot.leftMotor.SetSpeed(255)
    #robot.rightMotor.SetSpeed(255)
    time.sleep(1)
    robot.leftMotor.SetSpeed(0)
    robot.rightMotor.SetSpeed(0)
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        #draw.text((0, 0), "Zdec mozhet bit vasha reklama", font=font, fill=0)
        #draw.text((0, 8), "If vi ne Aram))0", font=font, fill=0)
        draw.ellipse([20,20,32,32],fill=255, outline=0)
        draw.ellipse([96,20,108,32],fill=255, outline=0)
        draw.ellipse([0,32,128,128],fill=255, outline=0)
        # Display image.
        disp.image(image)
        
        disp.display()
        
except KeyboardInterrupt:
    print('Ctrl+C pressed')

robot.Beep()

disp.clear()
disp.display()

robot.Release()
print('Stop EduBot')
