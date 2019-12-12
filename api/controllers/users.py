from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL
from flask import g

from api import constants
from api.controllers.base import BaseController
from api.status_codes import Status
from api.controllers import db_query_select

class UsersController(BaseController):

	def __init__(self):
		super(BaseController, self)

	def get(self, *args, **kwargs):
		if not BaseController.confirmAccessLevel(2):
			return super(UserController,self).error_response(Status.INVALID_TOKEN)
		return super(UsersController,self).get_all_users()
