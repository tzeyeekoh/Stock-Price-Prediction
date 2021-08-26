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
from .main_page import navbar
from .preprocess.preprocess import Preprocess
from .model.BuySellRegression import NeuralNet_Reg
from .config.load_conf import read_config

stock_details = html.Div(id='update-stock-details', className='content-container', 
    children=[])

pred_btn = html.Div(className='content-container', children=[dbc.Button("Predict", id='pred-reg-btn', color="success")])

pred_outcome = html.Div(id='pred-reg-output', className='content-container')

layout = html.Div([
    navbar,
    html.Br(),
    stock_details,
    pred_btn,
    pred_outcome
])

#############################################
@app.callback(
    Output('update-stock-details', 'children'),
    Input('nav-pred-reg', 'n_clicks')
)
def update_stk_details(n):
    conf = read_config()
    stk_details = [    
        html.H3('Selected Stock: '+ conf['StockData']['ticker']),
        html.H5('Historical period: '+ str(conf['StockData']['range'])),
        html.H5('Observation window: '+ str(conf['UserInput']['gain_window']) + " days"),
        html.H5('Buy/Sell Threshold: '+ str(conf['UserInput']['buy_threshold']*100) + "/" + str(conf['UserInput']['sell_threshold']*100) + "(%)"),
        html.Hr()
    ]
    return stk_details

@app.callback(
    Output('pred-reg-output', 'children'),
    Input('pred-reg-btn', "n_clicks")
)
def make_prediction_reg(n):
    conf = read_config()
    prep = Preprocess(conf)
    NN = NeuralNet_Reg()
