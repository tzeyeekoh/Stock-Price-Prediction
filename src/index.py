import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from src.app.app import app
from src.app import main_page
from src.app import reg_page

server = app.server
app.title = 'Stock Prediction'
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))

def display_page(pathname):
    '''Display for different pages
    '''
    print(pathname)
    if pathname == '/reg':
        return reg_page.layout
    return main_page.layout



if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')

'''To run:
set FLASK_APP=index.py 
flask run
'''