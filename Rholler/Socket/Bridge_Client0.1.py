import socket

def run_client():
    host = '47.27.194.250'  # Ion's external IP (NAT'd)
    port = 8713       # Arbitrary port number

    print("Searching for connection...")

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    # Confirm connection
    print("Connection established!")

    # Receive data from the server
    data = client_socket.recv(1024).decode()
    print("Received from server:", data)

    # Send data to the server
    message = "Hello test"
    client_socket.send(message.encode())

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    run_client()
