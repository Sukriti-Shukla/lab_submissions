from dash import dcc, html, Input, Output, State
from django_plotly_dash import DjangoDash
import plotly.express as px
import pandas as pd
import dash
# Sample data; replace this with your actual data
DATA = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [5, 4, 3, 2, 1],
    'z': [1, 2, 1, 2, 1],
})

# Name your Dash app (this name will be used to embed the app in Django)
app = DjangoDash('SimpleExample1')

# Define your Dash layout
app.layout = html.Div([
    dcc.Store(id='store-initial-data'),
    html.H1('Dash App'),
    html.Div(id='output-div')
])

@app.callback(
    Output('output-div', 'children'),
    [Input('store-initial-data', 'data')]
)
def update_output(data):
    print("Received Data in Dash:", data)  # Debugging line
    if not data:
        return "No data received"
    raw_data_path = data.get('raw_data_path', 'No path received')
    return f"Received path: {raw_data_path}"