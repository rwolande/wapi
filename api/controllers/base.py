import datetime, hashlib, uuid, jwt

from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL

from api import constants
from api.status_codes import Status
from api.controllers import db_query_select

class BaseController(Resource):

	def __init__(self):

		self.app = current_app

	def success_response(self, params={}):
		params['status'] = Status.SUCCESS.code
		return jsonify(params)

	def error_response(self, error_status, params={}):
		params['status'] = error_status.code
		params['message'] = error_status.message
		return jsonify(params)

	def get_salted_password(self,algorithm,salt,password):
		m = hashlib.new(algorithm)
		m.update(salt + password)
		password_hash = m.hexdigest()
		return password_hash

	def get_all_users(self):
		sql = 'SELECT * FROM' + constants.USER_TABLE + 'ORDER BY id DESC'
		users = db_query_select(sql)
		return self.success_response({"users":users})

	def encode_auth_token(self, user_id):
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=1800),
				'iat': datetime.datetime.utcnow(),
				'sub': user_id
			}
			return jwt.encode(
				payload,
				current_app.config['JWT_KEY'],
				algorithm='HS256'
			)
		except Exception as e:
			return e

	@staticmethod
	def decode_auth_token(auth_token):
		try:
			payload = jwt.decode(auth_token, current_app.config['JWT_KEY'])
			return payload['sub']
		except jwt.ExpiredSignatureError:
			return 'Signature expired. Please log in again.'
		except jwt.InvalidTokenError:
			return 'Invalid token. Please log in again.'

	@staticmethod
	def confirmAccessLevel(level):
		key = request.headers.get('JWT-Auth')
		if key is None:
			return None
		decoded_id = BaseController.decode_auth_token(key)
		sql = 'SELECT role FROM' + constants.USER_TABLE + 'WHERE id=%s LIMIT 1'
		params = (decoded_id,)
		res = db_query_select(sql,params)
		return res[0]["id"] >= level
