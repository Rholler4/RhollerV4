import socket
import pandas as pd
import plotly.express as px
from IPython.display import display, clear_output

# IP and port of the server
HOST = '192.168.0.101'
PORT = 49777

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Initialize empty lists to store data
distance1_data = []
distance2_data = []
angle0_data = []
angle1_data = []

# Receive data from the server continuously
while True:
    data = client_socket.recv(1024)
    if data:
        data = data.decode().split()
        distance1, distance2, angle0, angle1 = map(float, data)

        # Append received data to the lists
        distance1_data.append(distance1)
        distance2_data.append(distance2)
        angle0_data.append(angle0)
        angle1_data.append(angle1)

        # Create a DataFrame from the received data
        df = pd.DataFrame({
            'Distance1': distance1_data,
            'Distance2': distance2_data,
            'Angle0': angle0_data,
            'Angle1': angle1_data
        })

        # Plot the data using plotly.express
        fig = px.line(df, x='Angle0', y='Distance1', title='Servo Angles and Distances',
                      labels={'Angle0': 'Angle 0', 'Distance1': 'Distance 1'})
        fig.add_scatter(x=angle1_data, y=distance2_data, mode='lines', name='Distance 2 vs Angle 1')

        # Clear the previous plot and display the updated plot
        clear_output(wait=True)
        display(fig)
