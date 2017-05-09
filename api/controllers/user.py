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

		sql = 'SELECT * FROM' + constants.USER_TABLE + 'WHERE id= %s LIMIT 1'

		params = (user_id,)

		res = db_query_select(sql,params)

		if len(res) == 0:
			return super(UserController,self).error_response(Status.MISSING_PARAMETERS)

		user = res[0]
		return super(UserController,self).success_response({'user':user})

	def post(self, *args, **kwargs):

		body = request.get_json
		username = body['username']
		password = body['password']

		algorithm = 'sha512'  
		salt = uuid.uuid4().hex 

		m = hashlib.new(algorithm)
		m.update(salt + password)
		password_hash = m.hexdigest()
		final_password = "$".join([algorithm,salt,password_hash])

		sql = 'INSERT INTO' + constants.USER_TABLE + "(username,password) VALUES (\'" + username + "\',\'" + final_password + "\')"
		res = db_query_insert(sql)

		return super(UserController,self).error_response(Status.MISSING_PARAMETERS)

	# @protected
	# def put(self, *args, **kwargs):

	# 	# update user
	# 	set_string = ""

	# 	if get.sketch_image_source:
	# 		if len(set_string) > 0: 	
	# 			set_string = set_string + ","
	# 		set_string = set_string + "sketch_image_source=" + g.get.source_image_key

	# 	if get.name:
	# 		if len(set_string) > 0: 	
	# 			set_string = set_string + ","
	# 		set_string = set_string + "name=" + g.name

	# 	if(len(set_string) == 0):
	# 		return jsonify({'user':'no info received'})

	# 	sql = "UPDATE" + constants.USER_TABLE + set_string + " WHERE user_id=%s"
	# 	params(g.user_id,)
	# 	res = db_query_update(sql, params)

	# 	if res:
	# 		return jsonify({constants.QUERY_RESULT_STATUS_KEY:constants.QUERY_RESULT_SUCCESS_KEY })

	# @protected
	# def delete(self, *args, **kwargs):

	# 	return jsonify({'status':'failed'})

	# Helper methods


