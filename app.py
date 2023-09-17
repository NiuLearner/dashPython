import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data_url = (
    "https://raw.githubusercontent.com/NiuLearner/dashPython/main/Stocks.csv"
)
df_all = pd.read_csv(data_url)
# initial Dash
app = dash.Dash(__name__)
server = app.server
# figures
fig_price = px.line(df_all, x='Date', y='Close',
                    color='Ticker', title='Stock Price Over Time')
fig_volume = px.bar(df_all, x='Date', y='Volume',
                    color='Ticker', title='Stock Volume Over Time')
fig_stock_share = px.pie(df_all.groupby('Ticker').agg({'Close': 'mean'}).reset_index(
), values='Close', names='Ticker', title='Market Share by Stock')


# Dash outlayer
app.layout = html.Div([
    html.H1("Financial Dashboard"),
    dcc.Graph(id='price_graph', figure=fig_price),
    dcc.Graph(id='volume_graph', figure=fig_volume),
    dcc.Graph(id='stock_share_graph', figure=fig_stock_share)
])

if __name__ == '__main__':
    app.run_server(debug=True)
