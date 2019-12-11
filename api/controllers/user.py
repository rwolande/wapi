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
	def post(self, *args, **kwargs):

		username = g.username
		password = g.password

		hashed_password = self.getPasswordForUser(username)
		if not self.comparePasswords(password,hashed_password):
			return super(UserController,self).error_response(Status.BAD_PASSWORD)

		sql = 'SELECT id,username,role,password FROM' + constants.USER_TABLE + 'WHERE username=%s LIMIT 1'
		params = (username,)
		res = db_query_select(sql,params)
		if len(res) == 0:
			return super(UserController,self).error_response(Status.MISSING_PARAMETERS)

		user = res[0]
		return super(UserController,self).success_response({"user":user})

	def getPasswordForUser(self,username):
		sql = 'SELECT password FROM' + constants.USER_TABLE + 'WHERE username=%s LIMIT 1'
		params = (username,)
		res = db_query_select(sql,params)
		if len(res) == 0:
			return super(UserController,self).error_response(Status.MISSING_PARAMETERS)
		user = res[0]
		return user["password"]

	def comparePasswords(self,password,full):

		parts = full.split("$")
		algorithm = parts[0]
		salt = parts[1]
		password_hash = parts[2]

		m = hashlib.new(algorithm)
		m.update(salt + password)
		new_password_hash = m.hexdigest()

		return new_password_hash == password_hash