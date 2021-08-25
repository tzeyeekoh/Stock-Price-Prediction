from dash_bootstrap_components._components.Label import Label
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import yfinance as yf

from .app import app
from .preprocess.preprocess import Preprocess
from .config.load_conf import read_config

## Navigation bar
navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(dbc.NavLink("Prediction", href="/predict")),
        dbc.NavItem(dbc.NavLink("Train Model", href="/request")),
        
    ],
    brand="Stock Prediction",
    brand_href="/index",
    color="primary",
    dark=True,
)

ticker_selector = html.Div(
    id='ticker_selector',
    className='content-container',
    children=[
        html.H4('Stock Price Insights'),
        dbc.Row([
            dbc.Col([
                html.Label('Select Ticker'),
                html.Br(),
                dcc.Input(id='ticker-entry', placeholder='Select Ticker')
            ], width=2),
            dbc.Col([
                html.Label('Period'),
                dcc.Dropdown(
                    id='period-dropdown',
                    multi=False,
                    options=[{'label':'Max', 'value':'Max'}, 
                        {'label':'5-years', 'value':'5y'}, 
                        {'label':'1-year', 'value':'1y'}, 
                        {'label':'Year-to-date', 'value':'YTD'}, 
                        {'label':'6-months', 'value':'6m'}],
                    value='Max',
                    clearable= False)
            ], width=2),]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Label('Sell Threshold'),
                html.Br(),
                dcc.Input(id='sell-thresh-entry', type="number", value=10, min=1, max=999, step=1),
                html.Label('% Loss to sell')
            ], width=2),
            dbc.Col([
                html.Label('Buy Threshold'),
                html.Br(),
                dcc.Input(id='buy-threshold-entry', type="number", value=10, min=1, max=999, step=1),
                html.Label('% Gain to buy')
            ], width=2),
            dbc.Col([
                html.Label('Window'),
                html.Br(),
                dcc.Input(id='gain-window-entry', type="number", value=60, min=1, max=999, step=1),
                html.Label(' days')
            ], width=2),
        ]),
        
        html.Br(),
        dbc.Button('Get Data', 
            id="get-data-btn", 
            className="mr-1", 
            color='primary'),
        html.Hr(),
        dcc.Loading(className='loadscreen', type='circle', fullscreen=True,
            children=[
                html.Div(id="data-output", style={"verticalAlign": "middle"})
            ]),

    ])

layout = html.Div([
    navbar,
    html.Br(),
    ticker_selector
])

#############################################

@app.callback(
    Output("data-output", "children"), 
    Input("get-data-btn", "n_clicks"),
    State('ticker-entry', 'value'),
    State('period-dropdown', 'value'),
    State('sell-thresh-entry', 'value'),
    State('buy-threshold-entry', 'value'),
    State('gain-window-entry', 'value'),
    prevent_initial_call=True
)
def get_stock_data(n, ticker, period, sell_thresh, buy_thresh, gain_w):

    conf = read_config()
    prep = Preprocess(conf)
    print('Test click')
    print(ticker, period)

    buysell_thres = [-sell_thresh/100, buy_thresh/100]
    stk_data = prep._query_data(ticker, period_range=period)
    stk_data = prep._generate_features(stk_data, buysell_thres, gain_window=gain_w)

    fig = px.scatter(data_frame=stk_data.reset_index(), x="Date", y="Close", color="Rating")
    
    stk_insights = [
        html.H5('Company: '+ yf.Ticker(ticker).info['longName']+' | Period: '+period),
        html.Label("Sample data:"),
        dash_table.DataTable(
                data=stk_data.reset_index().sample(5).to_dict('records'),
                columns=[{'name': i, 'id': i} for i in stk_data.reset_index().columns],
                style_table={'overflowX': 'scroll'}),
        dcc.Graph(figure=fig)
    ]

    return stk_insights