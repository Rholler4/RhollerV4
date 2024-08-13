import socket
import random
import time

def generate_random_data():
    a = str(random.uniform(0, 90))  # Latitude
    b = str(random.uniform(0, 180))  # Longitude
    c = str(random.uniform(-90, 90))  # Tilt X
    d = str(random.uniform(-90, 90))  # Tilt Y
    e = str(random.uniform(20, 100))  # Temperature
    f = str(random.uniform(0, 100))  # CPU Usage
    g = str(random.uniform(0, 100))  # RAM Usage
    h = str(random.randint(0, 1))  # Headlight Power
    i = str(random.uniform(-45, 45))  # Steering Angle
    j = str(random.uniform(0, 100))  # Throttle
    k = str(random.randint(0, 10))  # Error Codes
    return f"{a},{b},{c},{d},{e},{f},{g},{h},{i},{j},{k}"


def run_client():
    host = '127.0.0.1'
    port = 8713

    print("Searching for connection...")

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("Connection established!")

        data = client_socket.recv(1024).decode()
        print("Received from server:", data)

        while True:
            message = generate_random_data()
            client_socket.send(message.encode())
            print(f"Sent to server: {message}")
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client_socket.close()
        print("Connection closed!")


if __name__ == "__main__":
    run_client()
