# Paired with Sonar_Socket_ServerX.py
# This script tests data sending over socket, then graphing with modifications for dual sensor data.
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import socket
import threading
import queue
import math  # Import math library for conversion

# Global variables to store the x and y values for two sensors
x_values_sensor1 = []
y_values_sensor1 = []
x_values_sensor2 = []
y_values_sensor2 = []


# Thread for handling socket communication
def socket_thread(q):  # Socket takes q as argument, which is a queue object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.0.101', 49730))  # Connect to the server
        while True:
            data = s.recv(1024).decode('utf-8').strip()
            if data:
                print("Received data:", data)  # Print the received data for diagnostics
                distance1, distance2, angle1, angle2 = map(float, data.split())

                # Convert from polar to Cartesian coordinates
                angle1_rad = math.radians(angle1)
                x1 = distance1 * math.cos(angle1_rad)
                y1 = distance1 * math.sin(angle1_rad)
                angle2_rad = math.radians(angle2)
                x2 = distance2 * math.cos(angle2_rad)
                y2 = distance2 * math.sin(angle2_rad)

                # Put the converted data into the queue
                q.put({'sensor1': (x1, y1), 'sensor2': (x2, y2)})


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

q = queue.SimpleQueue()


@app.callback(Output('real-time-graph', 'figure'),
              [Input('update-interval', 'n_intervals')])
def update_graph_live(n):
    global x_values_sensor1, y_values_sensor1, x_values_sensor2, y_values_sensor2, q

    if not n:
        print("Start thread...")
        threading.Thread(target=socket_thread, args=(q,), daemon=True).start()

    while not q.empty():
        p = q.get()
        # Update the plotting lists with Cartesian coordinates
        x_values_sensor1.append(p['sensor1'][0])
        y_values_sensor1.append(p['sensor1'][1])
        x_values_sensor2.append(p['sensor2'][0])
        y_values_sensor2.append(p['sensor2'][1])

    # Create new traces with updated data for both sensors
    trace1 = go.Scatter(x=x_values_sensor1, y=y_values_sensor1, mode='markers', name='Sensor 1')
    trace2 = go.Scatter(x=x_values_sensor2, y=y_values_sensor2, mode='markers', name='Sensor 2')

    return {
        'data': [trace1, trace2],  # Use the updated list of data for both sensors
        'layout': go.Layout(
            title='Real-time Data from Server',
            xaxis=dict(title='X coordinate', autorange=True),
            yaxis=dict(title='Y coordinate', autorange=True),
            uirevision='constant'  # Prevents resetting the zoom level after update
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
