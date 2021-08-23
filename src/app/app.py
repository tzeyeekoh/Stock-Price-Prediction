import flask
import dash
import dash_bootstrap_components as dbc

# from .config.config_load import read_yaml_file, YML_STR_LOAD

# doc = read_yaml_file()
# YML_STR = YML_STR_LOAD

server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.COSMO],
    server=server
)