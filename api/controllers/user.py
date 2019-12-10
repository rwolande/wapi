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

class UserController(BaseController):

	def __init__(self):
		super(BaseController, self)

	# @protected
	def get(self, user_id, *args, **kwargs):

		sql = 'SELECT id,role FROM' + constants.USER_TABLE + 'WHERE id= %s LIMIT 1'

		params = (user_id,)

		res = db_query_select(sql,params)

		if len(res) == 0:
			return super(UserController,self).error_response(Status.MISSING_PARAMETERS)

		user = res[0]
		return super(UserController,self).success_response(user)

