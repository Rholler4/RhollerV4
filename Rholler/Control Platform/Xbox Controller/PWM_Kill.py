import board
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C connection for the PCA9685
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the PCA9685 device
pca = PCA9685(i2c)
pca.frequency = 100  # Set frequency to 100 Hz

# Set duty cycle of all channels to 0
for channel in range(16):
    pca.channels[channel].duty_cycle = 0

print("All channels set to 0 duty cycle at 100 Hz")
