from flask import Flask,request,jsonify
from flask_cors import CORS
import imdb

import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback

import recommendation


server = Flask(__name__)
app = dash.Dash(__name__, server=server,
				title="Box Office Data Explorer",
				update_title='Updating...',
				suppress_callback_exceptions=True,
				external_stylesheets=[dbc.themes.QUARTZ])
CORS(server) 
ia = imdb.IMDb()

app.layout = html.Div(
	[
		html.H1('Simple Movie Recommendation System',   style = {"margin":"5% auto"}),
		html.Div(
				[dbc.Input(id="searchbarinput", placeholder="Type something...", type="text", style={"margin-right":"20px"}),
				dbc.Button("Search", id="searchbutton", size="lg", color="primary",  style = {"margin-inline":"auto", "width":"200px"}),
				],
		id="mainpage-searchbar",
		style = {"width":"70%", "margin-inline":"auto",  "display":"flex" }
		),
		html.Div([],
		id="searchdropdown",
		style={"width":"70%", "margin-inline":"auto",}
		),
		html.Div([],
		id="moviedetails",
		style={"width":"90%", "margin-inline":"auto",}
		)
	
	],
	id="page-content",
	style={"display": "flex", "flexDirection": "column", "height":"1440px", "background-image": "url(static/image.jpg)"},
)



#----------------------------------------
# Call back section
#----------------------------------------

@callback(
		Output("searchdropdown", "children"),
		[Input('searchbarinput', 'value')])
def get_movie_details(searchbarinput):
		if len(searchbarinput)==0:
			return
		else:
			search_movie = ia.search_movie(searchbarinput)
			if len(search_movie) ==0:
				list_group = dbc.ListGroup([dbc.ListGroupItem("Sorry, we can't not find that movie",action=True)])
			else:
				list_group = dbc.ListGroup(
										[
										dbc.ListGroupItem(str(i.data['title'])+' ('+str(i.data['year'])+')',action=True) for i in search_movie[:5] 
										])
			return list_group


@callback(
			output
)
#----------------------------------------
# Routing section
#----------------------------------------

@server.route('/movie', methods=['GET'])
def recommend_movies():
		res = recommendation.results(request.args.get('title'))
		return jsonify(res)

if __name__=='__main__':
		server.run(port = 5000, debug = True)
