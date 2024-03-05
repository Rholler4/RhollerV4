import socket

def run_server():
    host = '192.168.0.189'  # Ion's internal IP
    port = 8713       # Arbitrary port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server is listening for incoming connections...")

    # Accept a connection from the client
    conn, addr = server_socket.accept()
    print("Connected to:", addr)

    # Send data to the client
    message = "Hello, client! Welcome to the server."
    conn.send(message.encode())

    # Close the connection
    conn.close()

if __name__ == "__main__":
    run_server()
