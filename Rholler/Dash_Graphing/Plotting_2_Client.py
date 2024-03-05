import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import socket
import threading
import queue

# Set up the client
host = '192.168.0.101'  # Server's IP address
port = 49777        # Port number for the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Initialize a queue for storing the received x and y values
data_queue = queue.Queue(maxsize=20)

# Thread function for handling data reception
def receive_data():
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            x, y = map(int, data.split(','))
            # Immediately check queue before adding new data
            print(f"Queue size before adding new data: {data_queue.qsize()}")
            if data_queue.full():
                data_queue.get()  # Make room if needed
            data_queue.put((x, y))
            # Check after adding new data
            print(f"Added to queue: x = {x}, y = {y}. New queue size: {data_queue.qsize()}")


# Start the receiving thread
threading.Thread(target=receive_data, daemon=True).start()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    )
])

# Define the callback to update the graph
@app.callback(
    Output('live-update-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph_live(n):
    local_x = []
    local_y = []
    # Extract data from the queue
    while not data_queue.empty():
        x, y = data_queue.get()
        local_x.append(x)
        local_y.append(y)
        print(f"Graph Update: x = {x}, y = {y}")  # Additional debug print

    print(f"Updating graph with {len(local_x)} dynamic data points")  # Diagnostic print

    # Create a Plotly graph using the dynamic data
    figure = {
        'data': [
            go.Scatter(
                x=local_x,
                y=local_y,
                mode='lines+markers',
                name='Live Data'
            ),
            go.Scatter(
                x=[10],  # X coordinate of the static diagnostic point
                y=[20],  # Y coordinate of the static diagnostic point
                mode='markers',
                marker=dict(size=10, color='red'),
                name='Diagnostic Point'
            )
        ],
        'layout': go.Layout(
            title='Live Update Graph from Socket',
            xaxis=dict(title='X Value'),
            yaxis=dict(title='Y Value'),
        )
    }
    return figure



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
