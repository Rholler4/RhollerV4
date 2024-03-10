# This script just tests data sending over socket, then graphing. Not servo movement.
# Works with Plotly_test.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import socket
import json
import queue
import threading
import time

# Queue for holding data
data_queue = queue.Queue()


# Thread for handling socket communication
def socket_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.0.101', 49730))  # Connect to the server
        print("Connection established")
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
x_values = [5]  # Start with a static X value for diagnostics
y_values = [15]  # Start with a static Y value for diagnostics


@app.callback(Output('real-time-graph', 'figure'),
              [Input('update-interval', 'n_intervals')])
def update_graph_live(n):
    global x_values, y_values  # Use global variables to accumulate data

    print("Callback triggered")  # Confirm the callback is being triggered
    print("Queue size before entering loop:", data_queue.qsize())  # Check the size of the queue fixme: ALWAYS ZERO

    # Change this line from 'while data_queue.empty():' to the following
    while not data_queue.empty():  # This ensures the loop runs when the queue has data  fixme: NEVER ENTERS LOOP
        print("Entering the loop")  # This should print if the loop is entered
        try:
            data = data_queue.get_nowait()  # Use get_nowait() to avoid blocking
            print("Plotting data:", data)  # This will print the data being processed
            print("Data type of 'x':", type(data['x']), "Data type of 'y':", type(data['y']))
            x_values.append(data['x'])
            y_values.append(data['y'])
        except Exception as e:
            print(f"Error processing data from queue: {e}")
            break  # Exiting the loop if there's an error

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
