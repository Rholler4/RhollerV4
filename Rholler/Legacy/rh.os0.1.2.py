import socket
import random
from pydub import AudioSegment
from pydub.playback import play
import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
from adafruit_motorkit import MotorKit

ip = "192.168.0.190"
welcome_audio_files = [
    "Used_Lines/LWB1.wav",
    "Used_Lines/LWB2.wav",
    "Used_Lines/LWB3.wav",
    "Used_Lines/LWB4.wav",
    "Used_Lines/LWB5.wav",
    "Used_Lines/LWB6.wav",
]

# Prepare the Servos
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 100

# Throttle
channel_3 = hat.channels[3]
channel_3.duty_cycle = 0x24dd  # Idle at 14.4%

# Steering
channel_2 = hat.channels[2]
channel_2.duty_cycle = 0x1700  # Center Steering

# LED
channel_1 = hat.channels[1]
channel_1.duty_cycle = 0x0000  # LED off

# Unused
channel_0 = hat.channels[0]
channel_0.duty_cycle = 0x0000

# Getting kit ready for 12v supply / "motor controller"
kit = MotorKit()

# Start server
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((ip, 8888))
serv.listen(5)
print("SERVER: started")

while True:
    # Establish connection
    conn, addr = serv.accept()
    print("SERVER: connection to Client established")

    # Play welcome audio
    welcome_index = random.randint(0, len(welcome_audio_files) - 1)
    play(AudioSegment.from_wav(welcome_audio_files[welcome_index]))

    while True:
        # Receive data
        data = conn.recv(4096).decode()
        if not data:
            # Client disconnected
            break

        print("Received: " + data)

        # Headlights
        if data == 'LLH':
            kit.motor3.throttle = 0.5
        elif data == 'LLF':
            kit.motor3.throttle = 1
        elif data == 'LLO':
            kit.motor3.throttle = 0

        if data == 'RLH':
            kit.motor4.throttle = 0.5
        elif data == 'RLF':
            kit.motor4.throttle = 1
        elif data == 'RLO':
            kit.motor4.throttle = 0

        # Throttle Control
        if data == 'BFT' or data == 'BHT':
            channel_3.duty_cycle = 0
        elif data == 'FFT':
            channel_3.duty_cycle = 0x2710
        elif data == 'FHT':
            channel_3.duty_cycle = 0x26ac  # 26ac is the lowest possible throttle.
        elif data == 'NT':
            channel_3.duty_cycle = 0x24dd

        # Steering Control
        if data == 'ST' :
            channel_2.duty_cycle = 0x5888  # Center Steering
        elif data == 'RTF':
            channel_2.duty_cycle = 0x1124  # Right Full
        elif data == 'LTF':
            channel_2.duty_cycle = 0x26ac  # Left Full

    # Close connection when client disconnects
    conn.close()
    print("SERVER: Client disconnected")