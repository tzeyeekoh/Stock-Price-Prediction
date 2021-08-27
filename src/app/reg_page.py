import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

from .app import app
from .main_page import navbar
from .preprocess.preprocess import Preprocess
from .model.BuySellRegression import NeuralNet_Reg
from .config.load_conf import read_config

stock_details = html.Div(id='update-stock-details', className='content-container', 
    children=[])

pred_btn = html.Div(className='content-container', children=[
    dbc.Button("Predict", id='pred-reg-btn', color="success"),
    ])

pred_outcome = html.Div(className='content-container', children=[
    html.Br(),
    dcc.Loading(id='pred-reg-output', className='loadscreen', fullscreen= True,
        children=[])
])

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
        html.H5('Buy/Sell Threshold: '+ str(conf['UserInput']['buy_threshold']*100) + "/" + str(conf['UserInput']['sell_threshold']*100) + " (%)"),
        html.Hr()
    ]
    return stk_details

@app.callback(
    Output('pred-reg-output', 'children'),
    Input('pred-reg-btn', "n_clicks"),
    prevent_initial_call=True
)
def make_prediction_reg(n):
    conf = read_config()
    prep = Preprocess(conf)
    NN = NeuralNet_Reg(conf)

    ticker = conf['StockData']['ticker']
    X_train, X_test, y_train, y_test = prep.pipeline(ticker)
    model = NN.reg_NN(X_train)
    model = NN.train_NN(model, X_train, y_train)

    pred_y_train = model.predict(X_train)
    print(y_train, pred_y_train[:,0])

    future_gain = NN.predict_nextday(model, X_test)

    pred_output = [
        html.H5("Predicted gain: "+ str(future_gain*100)+"%")
    ]    

    return pred_output