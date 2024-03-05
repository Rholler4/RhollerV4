import socket

# IP and port of the server
HOST = '192.168.0.101'
PORT = 49777

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((HOST, PORT))

    # Receive data from the server continuously
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print('Received:', data.decode())

except KeyboardInterrupt:
    print("\nClient Interrupted")
except ConnectionResetError:
    print("Connection with the server reset.")
finally:
    # Close the client socket
    client_socket.close()
