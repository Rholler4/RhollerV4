# This script just tests data sending over socket, then graphing. Not servo movement.
# Works with Plotly_test.py
# ATTEMPTING TO PAIR WITH Sonar_Socket_Server1.py
# THIS ONE WORKS
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import socket
import json
import threading
import random
import queue

# Global variables to store the x and y values
x_values = [5]  # Start with a static X value for diagnostics
y_values = [15]  # Start with a static Y value for diagnostics


# Thread for handling socket communication
def socket_thread(q):  # Socket takes q as argument, which is queue object
    global x_values
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.0.101', 49730))  # Connect to the server
        while True:
            data = s.recv(1024).decode('utf-8')
            if data:
                print("Received data:", data)  # Print the received data for diagnostics
                # Convert JSON string back to dictionary and put it into the queue
                data_dict = json.loads(data)
                q.put(data_dict)


# Start the socket thread

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

# print(len(data_list))


q = queue.SimpleQueue()


@app.callback(Output('real-time-graph', 'figure'),
              [Input('update-interval', 'n_intervals')])
def update_graph_live(n):
    global x_values, y_values, q

    if not n:
        print("Start thread...")
        threading.Thread(target=socket_thread, args=(q,), daemon=True).start()

    # Copy and clear the shared list in a thread-safe manner

    if not q.empty():
        p = q.get()
        x_values.append(p['x'])
        y_values.append(p['y'])

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