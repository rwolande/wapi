import hashlib, uuid

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

	def getSaltedPassword(self,algorithm,salt,password):
		m = hashlib.new(algorithm)
		m.update(salt + password)
		password_hash = m.hexdigest()
		return password_hash

	def getAllUsers(self):
		sql = 'SELECT * FROM' + constants.USER_TABLE + 'ORDER BY id DESC'
		users = db_query_select(sql)
		return self.success_response({"users":users})