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

class RegisterController(BaseController):

	def __init__(self):
		super(BaseController, self)

	def post(self, *args, **kwargs):

		username = g.username
		password = g.password

		algorithm = 'sha512'  
		salt = uuid.uuid4().hex 

		m = hashlib.new(algorithm)
		m.update(salt + password)
		password_hash = m.hexdigest()
		final_password = "$".join([algorithm,salt,password_hash])

		sql = 'INSERT INTO' + constants.USER_TABLE + "(username,password) VALUES (\'" + username + "\',\'" + final_password + "\')"
		result_id = db_query_insert(sql)
		if not result_id is None:
			sql = 'SELECT * FROM' + constants.USER_TABLE + 'WHERE id= %s LIMIT 1'

			params = (result_id,)

			res = db_query_select(sql,params)

			if len(res) == 0:
				return super(RegisterController,self).error_response(Status.MISSING_PARAMETERS)

			user = res[0]
			return super(RegisterController,self).success_response(user)

		return super(RegisterController,self).error_response(Status.REGISTRATION_FAILED)

