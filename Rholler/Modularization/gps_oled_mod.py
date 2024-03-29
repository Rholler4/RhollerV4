# gps_oled_module.py

import time
import serial
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import busio
from board import SCL, SDA
import adafruit_gps


class GPSOLED:
    def __init__(self):
        # Initialize GPS
        self.uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10)
        self.gps = adafruit_gps.GPS(self.uart, debug=False)
        self.gps.send_command(b'PMTK314,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1')
        self.gps.send_command(b'PMTK220,1000')

        # Initialize OLED
        self.i2c = busio.I2C(SCL, SDA)
        # Add specific OLED initialization code here

    def update_display(self):
        # Update OLED display with GPS data
        pass

    def run(self):
        while True:
            self.update_display()
            time.sleep(1)

