# client_dash.py
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import socket
import json
import queue
import threading

# Queue for holding data
data_queue = queue.Queue()

# Thread for handling socket communication
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

# Start the socket thread
threading.Thread(target=socket_thread, daemon=True).start()

# Dash app for plotting
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='real-time-graph'),
    dcc.Interval(
        id='update-interval',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    )
])

# Global variables to store the x and y values
x_values = []
y_values = []


@app.callback(Output('real-time-graph', 'figure'),
              [Input('update-interval', 'n_intervals')])
def update_graph_live(n):
    global x_values, y_values  # Use global variables to accumulate data
    while not data_queue.empty():
        data = data_queue.get()
        print("Plotting data:", data)  # Print the data that will be plotted for diagnostics
        x_values.append(data['x'])
        y_values.append(data['y'])

    # Create a new trace with updated data
    trace = go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='Random Data')

    return {
        'data': [trace],  # Use the updated list of data
        'layout': go.Layout(
            title='Real-time Data from Server',
            xaxis=dict(title='Timestamp', autorange=True),
            yaxis=dict(title='Random Value', autorange=True),
            uirevision='constant'  # Prevents resetting the zoom level after update
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
