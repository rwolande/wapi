import hashlib, uuid

from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL
from flask import g

from api import constants
from api.controllers.base import BaseController
from api.status_codes import Status
from api.controllers import db_query_select

class LogInController(BaseController):

	def __init__(self):
		super(BaseController, self)

	# @protected
	def post(self, *args, **kwargs):

		username = g.username
		password = g.password

		hashed_password = self.get_password_for_user(username)
		if not self.compare_passwords(password,hashed_password):
			return BaseController.error_response(Status.BAD_PASSWORD)

		sql = 'SELECT id,username,role FROM' + constants.USER_TABLE + 'WHERE username=%s LIMIT 1'
		params = (username,)
		res = db_query_select(sql,params)
		if len(res) == 0:
			return super(LogInController,self).error_response(Status.MISSING_PARAMETERS)

		user = res[0]

		auth_token = BaseController.encode_auth_token(user["id"])
		user["auth_token"] = auth_token
		return BaseController.success_response({"user":user})

	def get_password_for_user(self,username):
		sql = 'SELECT password FROM' + constants.USER_TABLE + 'WHERE username=%s LIMIT 1'
		params = (username,)
		res = db_query_select(sql,params)
		if len(res) == 0:
			return BaseController.error_response(Status.MISSING_PARAMETERS)
		user = res[0]
		return user["password"]

	def compare_passwords(self,password,full):
		parts = full.split("$")
		algorithm = parts[0]
		salt = parts[1]
		password_hash = parts[2]
		new_password_hash = super(LogInController,self).get_salted_password(algorithm,salt,password)
		return new_password_hash == password_hash
