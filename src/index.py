import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from src.app.app import app
from src.app import main_page
# from src.app import request_page
# from src.app import account_page
# from src.app import predict_page

server = app.server
app.title = 'Stock Prediction'
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dcc.Store(id='file-update', data={}),
    dcc.Store(id='model-update', data={}),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))

def display_page(pathname):
    '''Display for different pages
    '''
    print(pathname)
    # if pathname == '/predict':
    #     return predict_page.layout
    # if pathname == '/request':
    #     return request_page.layout
    return main_page.layout



if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')

'''To run:
set FLASK_APP=index.py 
flask run
'''