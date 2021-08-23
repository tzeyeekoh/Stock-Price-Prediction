import pandas as pd
import dash_html_components as html
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

index_content = html.Div(
    id='index-container',
    className='content-container',
    children=[
        html.H4("Stock gain prediction")
    ])

layout = html.Div([
    navbar,
    html.Br(),
    index_content,
])

