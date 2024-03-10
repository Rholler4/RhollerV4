import socket
import dash
from dash import dcc, html
import plotly.graph_objs as go

# IP and port of the server
HOST = '192.168.0.101'
PORT = 49777

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize Dash app
app = dash.Dash(__name__)

# Initialize empty lists to store data
distance1_data = []
distance2_data = []
angle0_data = []
angle1_data = []

# Connect to the server
client_socket.connect((HOST, PORT))


# Receive data from the server continuously
@app.callback(
    dash.dependencies.Output('live-graph', 'figure'),
    [dash.dependencies.Input('live-graph-update', 'n_intervals')]
)
def update_graph(n):
    global distance1_data, distance2_data, angle0_data, angle1_data

    # Receive data from the server
    data = client_socket.recv(1024)
    print("Received data:", data)  # TODO: No data being printed
    if data:
        data = data.decode().split()
        print("Received data:", data)  # TODO: No data being printed
        distance1, distance2, angle0, angle1 = map(float, data)

        # Append received data to the lists
        distance1_data.append(distance1)
        distance2_data.append(distance2)
        angle0_data.append(angle0)
        angle1_data.append(angle1)

    # Create a Plotly figure
    fig = go.Figure()

    # Plot the data
    fig.add_trace(go.Scatter(x=angle0_data, y=angle1_data, mode='lines', name='Servo Angles'))
    fig.update_layout(title='Servo Angles',
                      xaxis_title='Angle 0',
                      yaxis_title='Angle 1')

    return fig


# Dash layout
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='live-graph-update',
        interval=1000,  # Update every 1 second
        n_intervals=0
    )
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
