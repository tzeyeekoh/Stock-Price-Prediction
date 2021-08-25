from dash_html_components.Label import Label
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

from .app import app

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
                dcc.Input(id='ticker', placeholder='Select Ticker')
            ], width=6),
            dbc.Col([
                html.Label('Period'),
                dcc.Dropdown(
                    id='period',
                    multi=False,
                    options=[{'label':'Max', 'value':'Max'}, 
                        {'label':'5-years', 'value':'5y'}, 
                        {'label':'1-year', 'value':'1y'}, 
                        {'label':'Year-to-date', 'value':'YTD'}, 
                        {'label':'6-months', 'value':'6m'}],
                    value='Max',
                    clearable= False)
            ], width=6)
        ])
        
    ])

layout = html.Div([
    navbar,
    html.Br(),
    ticker_selector
])

