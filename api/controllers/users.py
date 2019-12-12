from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL

from api import constants
from api.controllers.base import BaseController
from api.status_codes import Status
from api.controllers import db_query_select

class UsersController(BaseController):

	def __init__(self):
		super(BaseController, self)

	# @protected
	def get(self, user_id, *args, **kwargs):
		sql = 'SELECT * FROM' + constants.USER_TABLE + 'ORDER BY user_id ASC'
		users = db_query_select(sql)
		return super(UsersController,self).success_response({"users":users})
