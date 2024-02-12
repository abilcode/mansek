import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Sample data (replace this with your own dataset)
data = {
    'Date': pd.date_range(start='2021-01-01', end='2023-12-31', freq='D'),
    'Value': range(len(pd.date_range(start='2021-01-01', end='2023-12-31', freq='D')))  # 3 years of daily data
}
df = pd.DataFrame(data)

# Initialize the Dash app
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
    dcc.Graph(id='data-plot')
])


# Define callback to update the graph based on the dropdown value
@app.callback(
    Output('data-plot', 'figure'),
    [Input('group-by-dropdown', 'value')]
)
def update_graph(group_by):
    if group_by == 'year':
        grouped_data = df.groupby(df['Date'].dt.year)[["Value"]].sum()
        title = 'Data Grouped by Year'
    else:
        grouped_data = df.groupby([df['Date'].dt.year, df['Date'].dt.month])[["Value"]].sum()
        title = 'Data Grouped by Month'

    return {
        'data': [{
            'x': grouped_data.index,
            'y': grouped_data['Value'],
            'type': 'bar'
        }],
        'layout': {
            'title': title,
            'xaxis': {'title': 'Year' if group_by == 'year' else 'Month'},
            'yaxis': {'title': 'Sum of Values'}
        }
    }


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port =  9999)
