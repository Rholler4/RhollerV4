# Send raw tilt data in JSON for laptop to decide on
# Laptop will indicate tilt risk and display in tkinter

# rho_gyro

import board
import digitalio
import adafruit_lis3dh


class GyroSensor:
    def __init__(self, threshold=10):
        # Initialize I2C
        self.i2c = board.I2C()

        # Set the correct pin for the interrupt
        int1 = digitalio.DigitalInOut(board.D6)

        # Initialize LIS3DH accelerometer
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(self.i2c, int1=int1)
        self.lis3dh.range = adafruit_lis3dh.RANGE_4_G

        # Set the threshold for tilt detection
        self.threshold = threshold

    def read_acceleration(self):
        """
        Reads the current acceleration and checks for tilt and significant Z-axis acceleration.

        Returns:
            dict: A dictionary containing the x and y tilt, and a flag indicating if the device has been picked up.
        """
        x, y, z = self.lis3dh.acceleration  # Read acceleration values
        tilt_detected = self.check_tilt(x, y)
        picked_up = self.check_pick_up(z)

        return {"x_tilt": x, "y_tilt": y, "picked_up": picked_up}

    def check_tilt(self, x, y):
        """
        Checks if the device is tilting beyond the specified threshold.

        Parameters:
            x (float): Acceleration in the X direction.
            y (float): Acceleration in the Y direction.

        Returns:
            bool: True if tilt is beyond the threshold, False otherwise.
        """
        tilt = max(abs(x), abs(y))  # Simplified tilt calculation
        return tilt > self.threshold

    def check_pick_up(self, z, pick_up_threshold=2):
        """
        Checks for significant Z-axis acceleration, indicating the device might have been picked up.

        Parameters:
            z (float): Acceleration in the Z direction.
            pick_up_threshold (float): The acceleration threshold to indicate a pick up.

        Returns:
            bool: True if significant Z-axis acceleration is detected, False otherwise.
        """
        # Assuming normal Z acceleration due to gravity is 1g (~9.8 m/s^2),
        # and any significant increase might indicate a pick up.
        return abs(z) > pick_up_threshold
"""
HOW TO USE THIS SHIT

from gyro_module import GyroSensor

# Initialize the gyro sensor with a tilt threshold
gyro = GyroSensor(threshold=10)

# In your main loop or async task
sensor_data = gyro.read_acceleration()
print(sensor_data)  # Output the sensor data

# You can now include this data in your JSON payload
"""