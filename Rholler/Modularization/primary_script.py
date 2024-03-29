import socket

class CommandServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def run(self):
        while True:
            client, address = self.socket.accept()
            # Handle client in a new thread or process if non-blocking is needed
            command = client.recv(1024).decode('utf-8')
            # Process command
            client.close()
