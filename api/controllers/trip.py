from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL
from flask import g

from api import constants
from api.controllers.base import BaseController
from api.status_codes import Status
from api.controllers import db_query_select, db_query_insert, db_query_delete, db_query_update

class TripController(BaseController):

	def __init__(self):
		super(BaseController, self)

	def delete(self, trip_id, *args, **kwargs):
		sql = 'SELECT user_id' + constants.TRIP_TABLE + 'WHERE id=%s LIMIT 1'
		params = (trip_id),
		res = db_query_select(sql,params)
		user_id = res[0]["user_id"]
		
		sql = 'DELETE FROM' + constants.TRIP_TABLE + 'WHERE id=%s'

		params = (trip_id,)

		trips = db_query_delete(sql,params)

		sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE user_id=%s ORDER BY start_date ASC'
		params = (user_id,)
		trips = db_query_select(sql,params)
		return super(TripController,self).success_response({"trips":trips})

	def put(self, trip_id, *args, **kwargs):

		user_id = g.user_id
		destination = g.destination
		start_date = g.start_date
		end_date = g.end_date
		comment = g.comment

		sql = 'UPDATE' + constants.TRIP_TABLE + "SET destination=%s,start_date=%s,end_date=%s,comment=%s WHERE id=%s AND user_id=%s"
		params = (destination,start_date,end_date,comment,trip_id,user_id,)
		result_id = db_query_update(sql,params)
		if not result_id is None:
			sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE user_id=%s ORDER BY start_date ASC'
			params = (user_id,)
			trips = db_query_select(sql,params)
			return super(TripController,self).success_response({"trips":trips})

		return super(TripController,self).error_response(Status.MISSING_PARAMETERS)