import inputs
import socket
import json

# Function to categorize the ABS_Y value into throttle levels
def get_throttle_level(abs_y):
    if -32768 <= abs_y < -8000:
        return 'reverse'
    elif -8000 <= abs_y <= 8000:
        return 'neutral'
    elif 8000 < abs_y <= 32767:
        return 'forward'
    return 'neutral'  # Default case

# Function to categorize the ABS_RX value into steering directions
def get_steering_direction(abs_rx):
    if abs_rx < -5000:  # Left turn threshold
        return 'left'
    elif abs_rx > 5000:  # Right turn threshold
        return 'right'
    return 'straight'

def get_gamepad():
    last_sent_throttle = None
    last_sent_steering = None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('192.168.0.101', 49731))  # Replace with the Raspberry Pi's IP
            while True:
                events = inputs.get_gamepad()
                for event in events:
                    if event.ev_type == "Absolute":
                        if event.code == "ABS_Y":
                            throttle_command = get_throttle_level(event.state)
                            if throttle_command != last_sent_throttle:
                                data = {'throttle': throttle_command}
                                s.sendall(json.dumps(data).encode('utf-8'))
                                last_sent_throttle = throttle_command
                        elif event.code == "ABS_RX":
                            steering_command = get_steering_direction(event.state)
                            if steering_command != last_sent_steering:
                                data = {'steering': steering_command}
                                s.sendall(json.dumps(data).encode('utf-8'))
                                last_sent_steering = steering_command
    except KeyboardInterrupt:
        print("Controller script stopped")


if __name__ == "__main__":
    get_gamepad()
