import base64
import io
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from django_plotly_dash import DjangoDash
import plotly.express as px

app = DjangoDash('My_Dash_App')

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload File'),
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    dcc.Dropdown(
        id='sheet-dropdown',
        options=[],
        value=None,
        placeholder='Select a sheet'
    ),
    dcc.Dropdown(
        id='xaxis-dropdown',
        options=[],
        value=None,
        placeholder='Select column for X-axis'
    ),
    dcc.Dropdown(
        id='yaxis-dropdown',
        options=[],
        value=None,
        placeholder='Select column for Y-axis'
    ),
    dcc.Graph(id='graph-output'),
    # dcc.Input(id='file-path-store', type='text', style={'display': 'none'}),  # Hidden input to hold the filepath
    # html.Div(id='debug-output'),
    # html.Div(id='column-names-output')  # Div to display column names  # Div to hold the column names
    # dcc.Dropdown(
    #     id='dropdown-color',
    #     options=[
    #         {'label': 'Red', 'value': 'red'},
    #         {'label': 'Green', 'value': 'green'},
    #         {'label': 'Blue', 'value': 'blue'}
    #     ],
    #     value=None  # initial value will be set by initial_arguments
    # ),
    # html.Div(id='color-output')
])


@app.callback(
    [Output('sheet-dropdown', 'options'),
     Output('output-data-upload', 'children')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def upload_file(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        if 'xls' in filename:
            xls = pd.read_excel(io.BytesIO(decoded), sheet_name=None)
        else:
            return [], 'Invalid file type: Please upload an Excel file'
        
        sheet_options = [{'label': sheet, 'value': sheet} for sheet in xls.keys()]
        return sheet_options, f'Uploaded file contains {len(xls)} sheets.'
    return [], ''

@app.callback(
    Output('xaxis-dropdown', 'options'),
    [Input('sheet-dropdown', 'value')],
    [State('upload-data', 'contents')]
)
def update_xaxis_options(selected_sheet, contents):
    if contents is None:
        return []
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    xls = pd.read_excel(io.BytesIO(decoded), sheet_name=None)
    
    if selected_sheet in xls:
        column_options = [{'label': col, 'value': col} for col in xls[selected_sheet].columns]
        return column_options
    return []

@app.callback(
    Output('yaxis-dropdown', 'options'),
    [Input('sheet-dropdown', 'value')],
    [State('upload-data', 'contents')]
)
def update_yaxis_options(selected_sheet, contents):
    return update_xaxis_options(selected_sheet, contents)  # Reuse the same function for y-axis

@app.callback(
    Output('graph-output', 'figure'),
    [Input('xaxis-dropdown', 'value'),
     Input('yaxis-dropdown', 'value')],
    [State('sheet-dropdown', 'value'),
     State('upload-data', 'contents')]
)
def update_graph(x_column, y_column, selected_sheet, contents):
    if contents is None or x_column is None or y_column is None or selected_sheet is None:
        return px.scatter()  # Return an empty plot
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    xls = pd.read_excel(io.BytesIO(decoded), sheet_name=None)
    
    df = xls[selected_sheet]
    
    if x_column not in df.columns or y_column not in df.columns:
        return px.scatter()  # Return an empty plot

    # Check if the data is plot-able (should be numeric)
    if pd.api.types.is_numeric_dtype(df[x_column]) and pd.api.types.is_numeric_dtype(df[y_column]):
        return px.scatter(df, x=x_column, y=y_column)
    else:
        return px.scatter()  # Return an empty plot
@app.callback(
    Output('color-output', 'children'),
    [Input('dropdown-color', 'value')]
)
def display_color(selected_color):
    if selected_color is None:
        return "No color selected."
    return f"The selected color is {selected_color}."
# @app.callback(
#     Output('column-names-output', 'children'),
#     [Input('file-path-store', 'value')]
# )
# def display_column_names(filepath):
#     if filepath:
#         try:
#             df = pd.read_excel(filepath)  # Reading the first sheet by default
#             column_names = ', '.join(df.columns)
#             return f"The column names are: {column_names}"
#         except Exception as e:
#             return f"An error occurred: {e}"
#     return "No file path provided."