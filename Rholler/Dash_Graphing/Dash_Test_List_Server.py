import socket

# Server's IP address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 49700

# Set up the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")

    # Accept a connection
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break  # Connection closed
            conn.sendall(data)  # Echo back the received data
