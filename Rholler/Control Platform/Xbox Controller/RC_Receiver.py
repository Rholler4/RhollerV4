import socket
import json
import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit


def setup_pca():
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)
    pca.frequency = 100
    kit = ServoKit(channels=16)
    return pca.channels[11], kit.servo[10]


def adjust_throttle_from_command(channel, command):
    if command == 'neutral':
        duty_cycle = 0x2666
    elif command == 'forward':
        duty_cycle = 0x2800
    else:
        duty_cycle = 0x2666
    channel.duty_cycle = duty_cycle


def adjust_steering_from_command(servo, direction):
    # todo find servo angles to use for steering
    if direction == 'left':
        servo.angle = 45  # Adjust this angle for your setup
    elif direction == 'right':
        servo.angle = 135  # Adjust this angle for your setup
    else:
        servo.angle = 90  # Straight forward


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.168.0.101', 49731))
        s.listen()
        print("Waiting for connection...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            throttle_channel, steering_servo = setup_pca()
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    commands = json.loads(data.decode('utf-8'))
                    if 'throttle' in commands:
                        adjust_throttle_from_command(throttle_channel, commands['throttle'])
                    if 'steering' in commands:
                        adjust_steering_from_command(steering_servo, commands['steering'])
                except KeyError:
                    continue


if __name__ == "__main__":
    start_server()
