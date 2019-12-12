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

	def delete(self, user_id, *args, **kwargs):
		sql = 'DELETE FROM' + constants.USER_TABLE + 'WHERE id=%s'

		params = (user_id,)

		trips = db_query_delete(sql,params)

		sql = 'SELECT * FROM' + constants.USER_TABLE + 'ORDER BY user_id DESC'
		params = (user_id,)
		users = db_query_select(sql,params)
		return super(UserController,self).success_response({"users":users})

	def put(self, *args, **kwargs):
		username = g.username
		role = g.role

		sql = 'UPDATE' + constants.USER_TABLE + "SET username=%s,role=%s WHERE id=%s"
		params = (username,role,user_id)
		result_id = db_query_update(sql,params)
		if not result_id is None:
			sql = 'SELECT * FROM' + constants.USER_TABLE + 'ORDER BY user_id DESC'
			params = (user_id,)
			users = db_query_select(sql,params)
			return super(UserController,self).success_response({"users":users})
