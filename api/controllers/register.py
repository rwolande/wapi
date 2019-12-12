import hashlib, uuid

from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL
from flask import g

from api import constants
from api.controllers.base import BaseController
from api.status_codes import Status
from api.controllers import db_query_select, db_query_insert

class RegisterController(BaseController):

	def __init__(self):
		super(BaseController, self)

	def post(self, *args, **kwargs):

		username = g.username
		password = g.password
		role = g.role

		algorithm = 'sha512'  
		salt = uuid.uuid4().hex 

		m = hashlib.new(algorithm)
		m.update(salt + password)
		password_hash = m.hexdigest()
		final_password = "$".join([algorithm,salt,password_hash])

		sql = 'INSERT INTO' + constants.USER_TABLE + "(username,password,role) VALUES (\'" + username + "\',\'" + final_password + "\',\'"  + role + "\')"
		result_id = db_query_insert(sql)
		if result_id is None:
			return super(RegisterController,self).error_response(Status.REGISTRATION_FAILED)

		sql = 'SELECT id,username,role FROM' + constants.USER_TABLE + 'WHERE id=%s LIMIT 1'

		params = (result_id,)

		res = db_query_select(sql,params)

		if len(res) == 0:
			return super(RegisterController,self).error_response(Status.MISSING_PARAMETERS)

		user = res[0]
		return super(RegisterController,self).success_response({"user":user})

