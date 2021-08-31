import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

from .app import app
from .main_page import navbar
from .preprocess.preprocess import Preprocess
from .model.BuySellXGBoost import RandFor_Reg
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
    rf = RandFor_Reg(conf)
    #Init Model
    ticker = conf['StockData']['ticker']
    X_train, X_test, y_train, y_test = prep.pipeline(ticker)
    model = rf.rf_model()
    model = rf.train_rf(model, X_train, y_train)
    #Training Set
    pred_y_train= model.predict(X_train)
    df_val = pd.DataFrame({'Prediction':(pred_y_train)*100, 'Actual': (y_train)*100})
    fig = px.line(df_val, x=df_val.index, y='Actual', title= "Training Prediction")
    fig.add_scatter(x=df_val.index, y=df_val['Prediction'], name="Prediction")
    #Future movement
    future_gain, pred_movement = rf.predict_nextday(model, X_test)
    df_movement = pd.DataFrame({'Perc Change':pred_movement})
    fig_pred_movement = px.line(df_movement, x=df_movement.index, y='Perc Change', title="Predicted Movement")
    #Classify
    if future_gain >= conf['UserInput']['buy_threshold']:
        rec = "Buy"
    elif future_gain <= conf['UserInput']['sell_threshold']:
        rec = "Sell"
    else:
        rec = "Hold"

    pred_output = [
        dbc.Alert("Information provided on this website is general in nature and does not constitute financial advice.", color='danger'),
        html.H5("Predicted Movement: "+ str(future_gain*100)+"% in "+str(conf['UserInput']['gain_window']) + " days"),
        html.H5("Recommendation: "+rec),
        dcc.Graph(figure=fig),
        dcc.Graph(figure=fig_pred_movement),
    ]    

    return pred_output