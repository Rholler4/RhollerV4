# This is the server script. It pairs with anything using port 49730
import socket
import time
import random
import json

# Server's IP address and port
SERVER_HOST = '192.168.0.101'  # Listen on all network interfaces
SERVER_PORT = 49730

# Set up the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")
    conn, addr = server_socket.accept()

    with conn:
        print(f"Connected by {addr}")

        while True:
            # Generate random data
            data = {'x': random.randint(0, 6), 'y': random.randint(0, 10)}
            message = json.dumps(data)  # Convert dictionary to JSON string

            # Send data
            conn.sendall(message.encode('utf-8'))
            print(data)

            # Wait a bit before sending the next data
            time.sleep(1)

