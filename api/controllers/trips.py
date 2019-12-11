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

class TripsController(BaseController):

	def __init__(self):
		super(BaseController, self)

	# @protected
	def get(self, user_id, *args, **kwargs):

		sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE user_id=%s'

		params = (user_id,)

		trips = db_query_select(sql,params)

		if len(trips) == 0:
			return super(TripsController,self).error_response(Status.EMPTY_SET)

		return super(TripsController,self).success_response({"trips":trips})
