import socket
import time
import random

# Set up the server
host = '192.168.0.101'  # Server's IP address
port = 49777      # Port number for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Listening on {host}:{port}")

# Accept a client connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

try:
    while True:
        # Generate random x, y values
        x = random.randint(1, 100)
        y = random.randint(1, 100)

        # Create the message to send (format: "x,y")
        message = f"{x},{y}"

        # Send the message
        conn.sendall(message.encode('utf-8'))

        # Wait for a second before sending the next set of values
        time.sleep(1)
finally:
    # Close the connection
    conn.close()
    server_socket.close()
