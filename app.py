# Omisha Mondal om4kud
# import libraries
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
#import dash_bootstrap_components as dbc

# Read in the data
data = pd.read_csv('data.csv')

# add Quartz background theme layout
app = Dash(__name__)
server = app.server

# Add QUARTZ using the url
app.css.append_css({
    "external_url": "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/quartz/bootstrap.min.css"
})

# Make the layout
app.layout = dbc.Container([
    html.H1("Day Trader Graphs", style={'textAlign': 'center', 'marginBottom': '20px'}),  # Title for entire page
    dbc.Row([
        dbc.Col(
            dcc.RadioItems(
                id='radio-group-1',  # Radio buttons for Price and Change
                options=[
                    {'label': 'Price', 'value': 'Price'},
                    {'label': 'Change', 'value': 'Change'}
                ],
                value='Price',
                labelStyle={'display': 'inline-block', 'margin-right': '15px'}  # Increase space between radio buttons
            ),
            width=5,  # Center the radio buttons
            align='center'
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='company-symb',
                options=[
                    {'label': symbol, 'value': symbol} for symbol in data['Symbol'].unique() # creates a dropdown of the Symbol values using a dictionary
                ],
                value=[symbol for symbol in data['Symbol'].unique()[:3]],  # Select the first three symbols by default
                multi=True,  # Enable multi-select
                style={'color': 'black'}  # Set text color to black for readability
            ),
            width=5,  
            align='center' # Center the dropdown above graph 1
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='bubble-plot') # defines graph 1 in the column
        ),  
        dbc.Col(
            dcc.Graph(id='pe-ratio-graph') # defines graph 2 in the column
        )  
    ]),
])

# Callback for graph 1 bubble plot with radio buttons and company symbol dropdown
@app.callback(
    Output('bubble-plot', 'figure'),
    [Input('radio-group-1', 'value'),
     Input('company-symb', 'value')]
)
# Graph 1 update
def update_bubble_plot(filter, chose_symb):
    filtered_data = data[data['Symbol'].isin(chose_symb)] #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html
    
    fig = px.scatter(filtered_data, x='Price' if filter == 'Price' else 'Change', y='Market Cap', size='PE Ratio',
                     color='PE Ratio', hover_name='Symbol', title=f'Market Cap vs {filter} by PE Ratio')

    fig.update_layout(
        #Make the graph transparent against the chosen theme
        plot_bgcolor='rgba(0,0,0,0)',   # without this there would be a background color for the graph
        paper_bgcolor='rgba(0,0,0,0)',  # this makes sure the back part of the graph is transparent
        title_font=dict(size=20)  
    )
    return fig

# Define callback to update the PE Ratio graph
# incomplete
@app.callback(
    Output('pe-ratio-graph', 'figure'),
    [Input('radio-group-1', 'value')]
)

# graph 2 update
def update_pe_ratio_graph(filter):
    fig = px.histogram(data, x='PE Ratio', title='Distribution of PE Ratio')
    fig.update_layout(
        #Ensure the graph is fully transparent against the chosen theme
        plot_bgcolor='rgba(0,0,0,0)',   # without this there would be a background color for the graph
        paper_bgcolor='rgba(0,0,0,0)',  # this makes sure the back part of the graph is transparent
        title_font=dict(size=20)  
    )
    return fig

# Run the app
if __name__ == '__main__':
    #app.run_server(debug=True, port=8051)
    app.run_server(debug=True)
