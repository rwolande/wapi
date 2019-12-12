import hashlib
import uuid

from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL
from flask import g

from api import constants
from api.controllers.base import BaseController
from api.status_codes import Status
from api.controllers import db_query_select, db_query_insert, db_query_delete, db_query_update

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

	@protected
	def getPasswordForUser(self,username):
		sql = 'SELECT password FROM' + constants.USER_TABLE + 'WHERE username=%s LIMIT 1'
		params = (username,)
		res = db_query_select(sql,params)
		if len(res) == 0:
			return super(UserController,self).error_response(Status.MISSING_PARAMETERS)
		user = res[0]
		return user["password"]

	@protected
	def comparePasswords(self,password,full):

		parts = full.split("$")
		algorithm = parts[0]
		salt = parts[1]
		password_hash = parts[2]

		m = hashlib.new(algorithm)
		m.update(salt + password)
		new_password_hash = m.hexdigest()

		return new_password_hash == password_hash

	def delete(self, *args, **kwargs):
		user_id = g.user_id
		sql = 'DELETE FROM' + constants.USER_TABLE + 'WHERE id=%s'

		params = (user_id,)

		trips = db_query_delete(sql,params)

		sql = 'SELECT * FROM' + constants.USER_TABLE + 'ORDER BY user_id ASC'
		params = (user_id,)
		users = db_query_select(sql,params)
		return super(TripController,self).success_response({"users":users})

	def put(self, *args, **kwargs):

		user_id = g.user_id
		username = g.username
		role = g.role

		sql = 'UPDATE' + constants.USER_TABLE + "SET username=%s,role=%s WHERE id=%s"
		params = (username,role,user_id)
		result_id = db_query_update(sql,params)
		if not result_id is None:
			sql = 'SELECT * FROM' + constants.USER_TABLE + 'ORDER BY user_id ASC'
			params = (user_id,)
			users = db_query_select(sql,params)
			return super(TripController,self).success_response({"users":users})




