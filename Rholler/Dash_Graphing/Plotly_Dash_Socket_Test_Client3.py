import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import socket
import json
import queue
import threading

def socket_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.0.101', 49730))  # Connect to the server
        while True:
            data = s.recv(1024).decode('utf-8')
            if data:
                print("Received data:", data)  # Print the received data for diagnostics
                # Convert JSON string back to dictionary and put it into the queue
                data_dict = json.loads(data)
                data_queue.put(data_dict)
threading.Thread(target=socket_thread, daemon=True).start()