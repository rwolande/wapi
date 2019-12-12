from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL
from flask import g

from api import constants
from api.controllers.base import BaseController
from api.status_codes import Status
from api.controllers import db_query_insert, db_query_select

class TripsController(BaseController):

	def __init__(self):
		super(BaseController, self)

	# @protected
	def get(self, *args, **kwargs):

		user_id = g.user_id

		sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE user_id=%s ORDER BY start_date ASC'
		params = (user_id,)
		trips = db_query_select(sql,params)
		return super(TripsController,self).success_response({"trips":trips})

	def post(self, *args, **kwargs):

		user_id = g.user_id
		destination = g.destination
		start_date = g.start_date
		end_date = g.end_date
		comment = g.comment

		sql = 'INSERT INTO' + constants.TRIP_TABLE + "(user_id,destination,start_date,end_date,comment) VALUES (\'" + user_id + "\',\'" + destination + "\',\'" + start_date + "\',\'" + end_date + "\',\'" + comment + "\')"
		result_id = db_query_insert(sql)
		if not result_id is None:
			sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE user_id=%s ORDER BY start_date ASC'

			params = (user_id,)

			trips = db_query_select(sql,params)

			return super(TripsController,self).success_response({"trips":trips})

		return super(TripsController,self).error_response(Status.MISSING_PARAMETERS)
