import board
import busio
import adafruit_pca9685  # Import duty_cycle stuff
from adafruit_servokit import ServoKit  # Import servo stuff

i2c = busio.I2C(board.SCL, board.SDA)  # Initialize duty cycle
pwm = adafruit_pca9685.PCA9685(i2c)

# HIDDEN INSIDE ServoKit(channels=16) are default settings!
# One of which is a set to 50hz which doubled my 100hz duty cycle.
servos = ServoKit(channels=16)  # Renamed from kit
pwm.frequency = 100  # Renamed from hat.frequency


pwm.channels[11].duty_cycle = 0x2666  #FUNCTIONAL




servos.servo[2].angle = 15
