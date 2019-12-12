from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL

from api import constants
from api.controllers.base import BaseController
from api.status_codes import Status
from api.controllers import db_query_select

class TripsController(BaseController):

	def __init__(self):
		super(BaseController, self)

	# @protected
	def get(self, user_id, *args, **kwargs):
		sql = 'SELECT * FROM' + constants.TRIP_TABLE + 'WHERE user_id=%s ORDER BY start_date ASC'
		params = (user_id,)
		trips = db_query_select(sql,params)
		return super(TripsController,self).success_response({"trips":trips})
