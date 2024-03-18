# 3/18/2024 I only soldered pins for 12 of 16 pwm ports

from adafruit_servokit import ServoKit
import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 25kg red servos have range from 50-330hz
kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 270
kit.servo[1].actuation_range = 270
kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[1].set_pulse_width_range(500, 2500)


# Example to set LED brightness (using channels 6 to 11 for LEDs)
led_channels = range(6, 12)  # Channels 6 through 11
for channel in led_channels:
    # Set to full brightness, replace 0xffff with values from 0 to 0xffff to adjust brightness
    pca.channels[channel].duty_cycle = 0xffff
