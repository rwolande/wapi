import datetime

from flask import Flask, current_app
from flask import request
from flask import jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL
from flask import g
import hashlib
import uuid

#import db_query_select, db_query_update
from api.controllers.base import BaseController
from api import constants
from api.status_codes import Status
from api.controllers import db_query_select, db_query_insert

class TripController(BaseController):

	def __init__(self):
		super(BaseController, self)

	# @protected
	def get(self, user_id, *args, **kwargs):

		sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE user_id= %s'

		params = (user_id,)

		trips = db_query_select(sql,params)

		if len(trips) == 0:
			return super(UserController,self).error_response(Status.MISSING_PARAMETERS)

		return super(UserController,self).success_response(trips)

	def post(self, *args, **kwargs):

		user_id = g.user_id
		destination = g.destination
		startDate = g.startDate
		endDate = g.endDate
		comment = g.comment

		sql = 'INSERT INTO' + constants.TRIP_TABLE + "(user_id,destination,start_date,end_date,comment) VALUES (\'" + user_id + "\',\'" + destination + "\',\'" + start_date + "\',\'" + end_date + "\',\'" + comment + "\')"
		result_id = db_query_insert(sql)
		if not result_id is None:
			sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE id= %s LIMIT 1'

			params = (result_id,)

			trips = db_query_select(sql,params)

			if len(trips) == 0:
				return super(TripController,self).error_response(Status.MISSING_PARAMETERS)

			return super(TripController,self).success_response(trips)

		return super(TripController,self).error_response(Status.REGISTRATION_FAILED)
