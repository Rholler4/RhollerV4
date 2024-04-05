import inputs
import socket
import json

# Function to categorize the ABS_Y value into throttle levels
def get_throttle_level(abs_y):
    # Adjust these values based on your controller's range and sensitivity
    if -32768 <= abs_y < -8000:  # Brake zone
        return 'brake'
    elif -8000 <= abs_y <= 8000:  # Neutral zone
        return 'neutral'
    elif 8000 < abs_y <= 24000:  # Half throttle zone
        return 'half_forward'
    elif 24000 < abs_y <= 32767:  # Full throttle zone
        return 'full_forward'
    return 'neutral'  # Default case


def get_gamepad():
    last_sent_command = {'throttle': None, 'steering': None}  # Track the last commands sent for both throttle and steering
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Replace '192.168.0.101' with the IP address of the Raspberry Pi running the RC car script
            s.connect(('192.168.0.101', 49731))
            while True:
                events = inputs.get_gamepad()
                for event in events:
                    send_data = False  # Flag to track if we need to send data
                    command = {}
                    if event.ev_type == "Absolute" and event.code == "ABS_Y":
                        # Convert ABS_Y to a simple throttle command
                        throttle_command = get_throttle_level(event.state)
                        # Only send new commands if the throttle level changes
                        if throttle_command != last_sent_command['throttle']:
                            command['throttle'] = throttle_command
                            last_sent_command['throttle'] = throttle_command
                            send_data = True

                    # Handles steering. Not sure that Absolute is required
                    if event.ev_type == "Absolute" and event.code == "ABS_RX":
                        steering_command = 'left' if event.state < -8000 else 'right' if event.state > 8000 else 'neutral'
                        if steering_command != last_sent_command['steering']:
                            command['steering'] = steering_command
                            last_sent_command['steering'] = steering_command
                            send_data = True

                    if send_data:
                        # Send the command with a newline delimiter
                        s.sendall((json.dumps(command) + "\n").encode('utf-8'))
    except KeyboardInterrupt:
        print("Controller script stopped")


if __name__ == "__main__":
    get_gamepad()
