# import socket
# import threading
#
# data_list = []
#
# def socket_thread():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect(('127.0.0.1', 49700))  # Connect to the server
#
#         global data_list
#         data_list.append("x")
#         data_list.append("y")
#         print("hi")
#         print(len(data_list))


import socket

global data_list
data_list = []
# Server's IP address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 49700

data_to_send = b'Hello, server!'

# Set up the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Send data
    client_socket.sendall(data_to_send)

    data_list.append("x")
    data_list.append("y")
    print("hi")
    print(len(data_list))

    # Receive the response from the server and close the connection
    received_data = client_socket.recv(1024)
    print('Received', repr(received_data))

def update_graph_live(n):
    print("bye")
    print(len(data_list))
