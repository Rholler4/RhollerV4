import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # 1000 milliseconds = 1 second
        n_intervals=0
    )
])

# Define the callback to update the graph
@app.callback(
    Output('live-update-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph_live(n):
    # Generate some random data
    x_data = list(range(10))  # X values from 0 to 9
    y_data = [random.randint(1, 30) for _ in range(10)]  # Random Y values

    # Create a Plotly graph
    figure = {
        'data': [
            go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines+markers',
                name='Random Data'
            )
        ],
        'layout': go.Layout(
            title='Live Update Graph',
            xaxis=dict(title='X Axis'),
            yaxis=dict(title='Random Y Value'),
        )
    }
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
