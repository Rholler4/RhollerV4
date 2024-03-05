import socket
from inputs import get_gamepad

# Constants
IP_ADDRESS = "192.168.0.190"
PORT = 8888
BL = 0
BR = 0


# Commands
THROTTLE_COMMANDS = {
    'forward': {
        'half': "FHT",
        'full': "FFT",
        'neutral': "NT"
    },
    'reverse': {
        'half': "RHT",
        'full': "RFT",
        'neutral': "NT"
    }
}

STEERING_COMMANDS = {
    'right': {
        'full': "RTF",
        'half': "RTH",
        'stop': "ST"
    },
    'left': {
        'full': "LTF",
        'half': "LTH",
        'stop': "ST"
    }
}

LIGHTS_COMMANDS = {
    'left': {
        'half': "LLH",
        'full': "LLF",
        'off': "LLO"
    },
    'right': {
        'half': "RLH",
        'full': "RLF",
        'off': "RLO"
    }
}

def send_command(command):
    client.send(command.encode())

# Connect to the server
print("SERVER: standing by")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP_ADDRESS, PORT))
print("CLIENT: connected")

try:
    while True:
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)

            # Throttle Control
            if event.code == 'ABS_Y':
                if event.state < 0:
                    # Reverse
                    print("Uhh we aren't doing that yet")
                else:
                    # Forward
                    throttle_percent = int(100 * (event.state / 32767)) / 100
                    if 0.5 < throttle_percent < 0.8:
                        print("Forward Half Throttle")
                        send_command(THROTTLE_COMMANDS['forward']['half'])
                    elif throttle_percent >= 0.8:
                        print("Forward Full Throttle")
                        send_command(THROTTLE_COMMANDS['forward']['full'])
                    else:
                        print("Neutral Throttle")
                        send_command(THROTTLE_COMMANDS['forward']['neutral'])

            # Steering Control
            if event.code == 'ABS_RX':
                if event.state in range(25001, 32767):
                    print("Right Turn Full")
                    send_command(STEERING_COMMANDS['right']['full'])
                elif event.state in range(15000, 25001):
                    print("Right Turn Half")
                    send_command(STEERING_COMMANDS['right']['half'])
                elif event.state in range(-32768, -25000):
                    print("Left Turn Full")
                    send_command(STEERING_COMMANDS['left']['full'])
                elif event.state in range(-25000, -14999):
                    print("Left Turn Half")
                    send_command(STEERING_COMMANDS['left']['half'])
                else:
                    print("STOP Turn")
                    send_command(STEERING_COMMANDS['left']['stop'])

            # Button Events
            if event.ev_type == "Key":
                if event.code == 'BTN_SOUTH' and event.state == 1:
                    print("Button A")

                if event.code == 'BTN_EAST' and event.state == 1:
                    print("Button B")

                if event.code == 'BTN_WEST' and event.state == 1:
                    print("Emergency Stop")
                    send_command("SP")

                # Headlights
                # This is using BL
                if event.code == 'BTN_TL' and event.state == 1:
                    if BL == 0:
                        print("Turning L light to half")
                        BL = 1
                        send_command(LIGHTS_COMMANDS['left']['half'])
                    elif BL == 1:
                        print("Turning L light to full")
                        BL = 2
                        send_command(LIGHTS_COMMANDS['left']['full'])
                    elif BL == 2:
                        print("Turning L light off")
                        BL = 0
                        send_command(LIGHTS_COMMANDS['left']['off'])

                if event.code == 'BTN_TR' and event.state == 1:
                    if BR == 0:
                        print("Turning R light to half")
                        BR = 1
                        send_command(LIGHTS_COMMANDS['right']['half'])
                    elif BR == 1:
                        print("Turning R light to full")
                        BR = 2
                        send_command(LIGHTS_COMMANDS['right']['full'])
                    elif BR == 2:
                        print("Turning R light off")
                        BR = 0
                        send_command(LIGHTS_COMMANDS['right']['off'])

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Close the connection
    client.close()
