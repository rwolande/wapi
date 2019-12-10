from flask import Flask, current_app, request, jsonify, g
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL

import jwt
import bcrypt

from api.controllers.base import BaseController
from api.controllers.user import UserController
from api.controllers.register import RegisterController
from api.controllers.trip import TripController
from api.controllers.trips import TripsController

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py')

# Loads the configration from /instance/config.py
# NOTE: This file is not checked into git - it must 
# be defined for every installation

app.api = Api(app)
app.mysql = MySQL(app)

# define routes
app.api.add_resource(UserController, '/user/<int:user_id>')
app.api.add_resource(RegisterController, '/register')
app.api.add_resource(TripController, '/trip')
app.api.add_resource(TripsController, '/trips/<int:user_id>')

@app.before_request
def before_request():

	# Add anything you want to parse from the POST body
	# to this array and it will be available in flask.g
	post_parameters = ['username',
					   'password',
					   'role',
					   'user_id',
					   'destination'
					   'start_date',
					   'end_date',
					   'comment',]
					   
	if not request.method == 'GET':
		for param in post_parameters:
			value = request.json[param] if param in request.json else None
			setattr(g,param,value)

if __name__ == '__main__':
	app.debug = True
 	app.run()

