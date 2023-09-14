import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data_url = "https://raw.githubusercontent.com/NiuLearner/dashPython/main/Stocks.csv"
df_all = pd.read_csv(data_url)

available_tickers = df_all['Ticker'].unique()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Financial Dashboard"),
    

    html.Label("Select Stock Tickers:"),
    dcc.Dropdown(
        id='ticker_dropdown',
        options=[{'label': i, 'value': i} for i in available_tickers],
        value=available_tickers, 
        multi=True  
    ),
    
    dcc.Graph(id='price_graph'),
    dcc.Graph(id='volume_graph'),
    dcc.Graph(id='stock_share_graph')
])

@app.callback(
    [Output('price_graph', 'figure'),
     Output('volume_graph', 'figure'),
     Output('stock_share_graph', 'figure')],
    [Input('ticker_dropdown', 'value')]
)
def update_graph(selected_tickers):
    filtered_df = df_all[df_all['Ticker'].isin(selected_tickers)]
    
    fig_price = px.line(filtered_df, x='Date', y='Close',
                        color='Ticker', title='Stock Price Over Time')
    
    fig_volume = px.bar(filtered_df, x='Date', y='Volume',
                        color='Ticker', title='Stock Volume Over Time')
    
    fig_stock_share = px.pie(filtered_df.groupby('Ticker').agg({'Close': 'mean'}).reset_index(),
                             values='Close', names='Ticker', title='Market Share by Stock')
    
    return fig_price, fig_volume, fig_stock_share

if __name__ == '__main__':
    app.run_server(debug=True)
