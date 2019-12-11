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

	def post(self, *args, **kwargs):

		user_id = g.user_id
		destination = g.destination
		start_date = g.start_date
		end_date = g.end_date
		comment = g.comment

		sql = 'INSERT INTO' + constants.TRIP_TABLE + "(user_id,destination,start_date,end_date,comment) VALUES (\'" + user_id + "\',\'" + destination + "\',\'" + start_date + "\',\'" + end_date + "\',\'" + comment + "\')"
		result_id = db_query_insert(sql)
		if not result_id is None:
			sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE id=%s LIMIT 1'

			params = (result_id,)

			trips = db_query_select(sql,params)

			return super(TripController,self).success_response({"trips":trips})

		return super(TripController,self).error_response(Status.MISSING_PARAMETERS)
