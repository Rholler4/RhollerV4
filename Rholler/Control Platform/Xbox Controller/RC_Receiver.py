import socket
import json
import board
import busio
import adafruit_pca9685

def setup_pca():
    i2c = busio.I2C(board.SCL, board.SDA)
    hat = adafruit_pca9685.PCA9685(i2c)
    hat.frequency = 100
    return hat.channels[11]

def adjust_throttle_from_command(channel, command):
    # Adjust the throttle based on the received command
    if command == 'neutral':
        duty_cycle = 0x2666
    elif command == 'forward':
        duty_cycle = 0x2800
    # elif command == 'reverse':
        # Replace 0x2000 with the actual duty cycle for reverse if different
    #   duty_cycle = 0x2000
    else:
        # Default to neutral if command is unrecognized
        duty_cycle = 0x2666
    channel.duty_cycle = duty_cycle

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 50123))
        s.listen()
        print("Waiting for connection...")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            throttle_channel = setup_pca()
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Extract the throttle command and adjust the throttle
                try:
                    command = json.loads(data.decode('utf-8'))['throttle']
                    adjust_throttle_from_command(throttle_channel, command)
                except KeyError:
                    # If 'throttle' key is not found in the received data, ignore it
                    continue

if __name__ == "__main__":
    start_server()
