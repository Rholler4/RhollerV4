import gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from adafruit_servokit import ServoKit
from time import sleep
import socket
import adafruit_pca9685

# Set gpiozero to use the pigpio pin factory
gpiozero.Device.pin_factory = PiGPIOFactory()

# Initialize distance sensors with the pigpio pin factory
sensor1 = DistanceSensor(echo=27, trigger=17)
sensor2 = DistanceSensor(echo=23, trigger=22)

# Initialize servos
kit = ServoKit(channels=16)
# Set frequency to 100!!!!!
# TODO test to see if this doesn't fuck the throttle
pca = adafruit_pca9685.PCA9685(busio.I2C(board.SCL, board.SDA))
pca.frequency = 100
kit.servo[0].actuation_range = 270
kit.servo[1].actuation_range = 270
kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[1].set_pulse_width_range(500, 2500)

# Set initial servo angles
current_angle_0 = 0
current_angle_1 = 0
kit.servo[0].angle = current_angle_0
kit.servo[1].angle = current_angle_1

# Set the increment and initialize direction
increment = 15
direction_0 = 1
direction_1 = 1

# Socket initialization
HOST = '192.168.0.101'  # IP address of the server
PORT = 49730  # Port to listen on

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

try:
    while True:
        # Accept incoming connection
        conn, addr = server_socket.accept()
        print('Connected by', addr)

        while True:  # Continuously send data to the client
            # Read and print distance from both sensors
            distance1 = sensor1.distance * 100  # Convert to centimeters
            distance2 = sensor2.distance * 100  # Convert to centimeters
            print(f'Distance from sensor 1: {distance1:.1f} cm')
            print(f'Distance from sensor 2: {distance2:.1f} cm')

            # Send data to the client
            data_to_send = f'{distance1:.1f} {distance2:.1f} {current_angle_0} {current_angle_1}\n'
            conn.sendall(data_to_send.encode('utf-8'))

            # Wait a bit for the distance to stabilize
            sleep(0.5)

            # Update and set new angles for servos
            current_angle_0 += increment * direction_0
            current_angle_1 += increment * direction_1

            # Reverse direction if the end is reached
            if current_angle_0 >= 270 or current_angle_0 <= 0:
                direction_0 *= -1
                current_angle_0 = max(0, min(270, current_angle_0))  # Keep within [0, 270]

            if current_angle_1 >= 270 or current_angle_1 <= 0:
                direction_1 *= -1
                current_angle_1 = max(0, min(270, current_angle_1))  # Keep within [0, 270]

            # Apply the new angles
            kit.servo[0].angle = current_angle_0
            kit.servo[1].angle = current_angle_1

            # Wait before taking the next readings and making the next movement
            sleep(1)

except KeyboardInterrupt:
    # Set both servos to 135 degrees on interrupt
    kit.servo[0].angle = 135
    kit.servo[1].angle = 135
    print("\nExiting program and setting servos to 135 degrees")
finally:
    # Close the server socket
    server_socket.close()
