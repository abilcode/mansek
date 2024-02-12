import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Sample DataFrame
df = pd.read_csv(
    "used_data.csv",
    parse_dates=["funded_date"]
)

# Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='group-by-dropdown',
        options=[
            {'label': 'Year', 'value': 'year'},
            {'label': 'Month', 'value': 'month'}
        ],
        value='year',  # Default value
        style={'width': '200px'}
    ),
    dcc.Graph(id='interest-plot'),
    dcc.Graph(id='ltv-plot'),
    dcc.Graph(id='yield-plot'),
])

# Define callback to update the Interest income plot
@app.callback(
    Output('interest-plot', 'figure'),
    [Input('group-by-dropdown', 'value')]
)
def update_graph_interest(group_by):
    if group_by == 'year':
        data_used = df.copy()
        grouped_data = data_used.groupby(data_used['funded_date'].dt.year)[["interest_income"]].sum()
        title = 'Interest Income Grouped by Year'
    else:
        data_used  = df.copy()
        # Group by month and sum the income
        grouped_data = data_used.groupby(data_used['funded_date'].dt.month)[["interest_income"]].sum()
        title = 'Interest Income Grouped by Month'

    return {
        'data': [{
            'x': grouped_data.index,
            'y': grouped_data['interest_income'],
            'type': 'line'
        }],
        'layout': {
            'title': title,
            'xaxis': {'title': 'Year' if group_by == 'year' else 'Month'},
            'yaxis': {'title': 'Sum of Values'}
        }
    }

# Define callback to update the LTV plot
@app.callback(
    Output('ltv-plot', 'figure'),
    [Input('group-by-dropdown', 'value')]
)
def update_graph_ltv(group_by):
    if group_by == 'year':
        data_used = df.copy()
        grouped_data = data_used.groupby(data_used['funded_date'].dt.year)[["LTV_ratio"]].sum()
        title = 'LTV ratio Grouped by Year'
    else:
        data_used  = df.copy()
        # Group by month and sum the income
        grouped_data = data_used.groupby(data_used['funded_date'].dt.month)[["LTV_ratio"]].sum()
        title = 'LTV ratio Grouped by Month'

    return {
        'data': [{
            'x': grouped_data.index,
            'y': grouped_data['LTV_ratio'],
            'type': 'line'
        }],
        'layout': {
            'title': title,
            'xaxis': {'title': 'Year' if group_by == 'year' else 'Month'},
            'yaxis': {'title': 'Sum of Values'}
        }
    }

# Define callback to update the yield plot
@app.callback(
    Output('yield-plot', 'figure'),
    [Input('group-by-dropdown', 'value')]
)
def update_graph_yield(group_by):
    if group_by == 'year':
        data_used = df.copy()
        grouped_data = data_used.groupby(data_used['funded_date'].dt.year)[["interest_income","funded_amount"]].sum()
        title = 'Portofolio Yield Grouped by Year'
    else:
        data_used  = df.copy()
        # Group by month and sum the income
        grouped_data = data_used.groupby(data_used['funded_date'].dt.month)[["interest_income","funded_amount"]].sum()
        title = 'Portofolio Yield Grouped by Month'

    return {
        'data': [{
            'x': grouped_data.index,
            'y': grouped_data['interest_income'] / grouped_data['funded_amount'],
            'type': 'line'
        }],
        'layout': {
            'title': title,
            'xaxis': {'title': 'Year' if group_by == 'year' else 'Month'},
            'yaxis': {'title': 'Sum of Values'}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True, port = 8050)
