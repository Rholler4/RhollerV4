# Then ready data in JSON to send to tkinter

# temp_sensor_module.py

import board
import adafruit_mcp9808


class TempSensor:
    def __init__(self):
        # Initialize I2C
        self.i2c = board.I2C()

        # Initialize MCP9808 temperature sensor
        self.sensor = adafruit_mcp9808.MCP9808(self.i2c)

    def read_temperature(self):
        """
        Reads the current temperature from the sensor.

        Returns:
            float: The current temperature in Fahrenheit.
        """
        tempC = self.sensor.temperature
        tempF = tempC * 9 / 5 + 32
        return tempF

"""
HOW TO USE THIS SHIT

from temp_sensor_module import TempSensor

# Initialize the temperature sensor
temp_sensor = TempSensor()

# In your main loop or async task
current_temp = temp_sensor.read_temperature()
print(f"Current Temperature: {current_temp} F")

# Now, you can include this temperature data in your JSON payload

"""