from flask import Flask,request,jsonify
from flask_cors import CORS
import recommendation

import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, State
from dash import dcc, dash_table

server = Flask(__name__)
app = dash.Dash(__name__, server=server,
                title="Box Office Data Explorer",
                update_title='Updating...',
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.QUARTZ])
CORS(server) 

app.layout = html.Div(
    [
        html.H1('Some title'),
        html.Div(
        [dbc.Input(id="inputbar", placeholder="Type something...", type="text")],
        id="mainpage-searchbar",
        style = {"width":"70%", "margin":"10% auto" }
        ),
        html.Div(
        [dbc.Button("searchbutton",  size="lg", color="primary",  style = {"margin-inline":"auto", "width":"200px"})],
        id="mainpage-searchbutton",
        style = {"margin-inline":"auto"}
        )
    ],
    id="page-content",
    style={"display": "flex", "flexDirection": "column", "height":"1440px", "background-image": "url(static/image.jpg)"},
)


@server.route('/movie', methods=['GET'])
def recommend_movies():
        res = recommendation.results(request.args.get('title'))
        return jsonify(res)

if __name__=='__main__':
        server.run(port = 5000, debug = True)
