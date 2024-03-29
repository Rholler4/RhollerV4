import time
import board
import digitalio
import adafruit_lis3dh

# Initialize I2C
i2c = board.I2C()

# Set the correct pin for the interrupt
int1 = digitalio.DigitalInOut(board.D6)

# Initialize LIS3DH accelerometer
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

# Set the range of the accelerometer to provide more sensitivity.
# The options are: RANGE_2_G, RANGE_4_G, RANGE_8_G, or RANGE_16_G
lis3dh.range = adafruit_lis3dh.RANGE_4_G


def check_tilt(x, y, z, threshold=10):
    """
    Check if the RC car is tilting beyond a specified threshold.
    Parameters:
        x, y, z: Accelerometer readings along the X, Y, and Z axes.
        threshold: The tilt threshold to trigger a warning (in degrees).
    Returns:
        A boolean indicating whether the car is tilting too much.
    """
    # Calculate the tilt. This is a basic implementation and might need
    # adjustment depending on the orientation of the accelerometer
    # and how you define "too much tilt."
    tilt = max(abs(x), abs(y))  # Simplified tilt calculation

    # Check if the tilt exceeds the threshold
    if tilt > threshold:
        return True
    return False


# Main loop to read accelerometer values and check for tilt
while True:
    x, y, z = lis3dh.acceleration  # Read acceleration values
    if check_tilt(x, y, z):
        print("Tilt detected!")
    else:
        print("No significant tilt.")

    time.sleep(0.5)  # Pause for half a second
