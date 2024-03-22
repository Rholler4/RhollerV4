import socket
import json
import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit


def setup_pca():
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)
    kit = ServoKit(channels=16)
    pca.frequency = 100  # ALWAYS set frequency after servokit
    return pca.channels[11], kit.servo[2]


def adjust_throttle_from_command(channel, command):
    if command == 'neutral':
        duty_cycle = 0x2666  # Neutral signal
    elif command == 'half_forward':
        duty_cycle = 0x2800  # Half forward signal
    elif command == 'full_forward':
        duty_cycle = 0x2900  # Full forward signal
    elif command == 'brake':
        duty_cycle = 0x1999  # Brake signal
    else:
        duty_cycle = 0x2666  # Default to neutral
    channel.duty_cycle = duty_cycle



def adjust_steering_from_command(servo, direction):
    # todo find servo angles to use for steering
    if direction == 'left':
        print("left")
        servo.angle = 30  # Adjust this angle for your setup
    elif direction == 'right':
        print("right")
        servo.angle = 0  # Adjust this angle for your setup
    else:
        servo.angle = 15  # Straight forward


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.168.0.101', 49731))
        s.listen()
        print("Waiting for connection...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            throttle_channel, steering_servo = setup_pca()
            buffer = ""  # Initialize an empty buffer
            while True:
                chunk = conn.recv(1024).decode('utf-8')  # Receive data
                if not chunk:
                    break  # Disconnect if no data
                buffer += chunk  # Add data to buffer
                while "\n" in buffer:  # Check if there's a complete message
                    message, buffer = buffer.split("\n", 1)  # Split by the first newline
                    try:
                        commands = json.loads(message)  # Try to decode JSON
                        if 'throttle' in commands:
                            adjust_throttle_from_command(throttle_channel, commands['throttle'])
                        if 'steering' in commands:
                            adjust_steering_from_command(steering_servo, commands['steering'])
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
                    except KeyError:
                        continue  # Skip if the necessary keys aren't present



if __name__ == "__main__":
    start_server()
