# temp_module.py

import time
import board
import adafruit_mcp9808

class TempSensor:
    def __init__(self):
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_mcp9808.MCP9808(self.i2c)

    def read_temperature(self):
        # Read temperature from the sensor
        pass

    def run(self):
        while True:
            self.read_temperature()
            time.sleep(1)
