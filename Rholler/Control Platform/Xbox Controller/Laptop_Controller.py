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

def get_gamepad():
    last_sent_command = None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Replace '192.168.1.100' with the IP address of the Raspberry Pi running the RC car script
            s.connect(('192.168.1.101', 50123))
            while True:
                events = inputs.get_gamepad()
                for event in events:
                    if event.ev_type == "Absolute" and event.code == "ABS_Y":
                        # Convert ABS_Y to a simple throttle command
                        throttle_command = get_throttle_level(event.state)
                        # Only send new commands if the throttle level changes
                        if throttle_command != last_sent_command:
                            data = {'throttle': throttle_command}
                            s.sendall(json.dumps(data).encode('utf-8'))
                            last_sent_command = throttle_command
    except KeyboardInterrupt:
        print("Controller script stopped")

if __name__ == "__main__":
    get_gamepad()
