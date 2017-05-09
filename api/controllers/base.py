from flask import Flask, current_app, request, jsonify
from flask_restful import Resource

from api.status_codes import Status

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