import math
from functools import wraps

from flask import Flask, current_app, request, jsonify, g
from flask_restful import Resource, Api, reqparse, HTTPException
from flask_mysqldb import MySQL
from _mysql_exceptions import IntegrityError

from api.controllers.base import BaseController

import jwt
import bcrypt

from api import constants
from api.status_codes import Status

def check_params_type(params):
	"""Raises an exception if passed something besides a tuple"""

	if params and type(params) is not tuple:
		msg = "db_query_* functions require the params arg to be a tuple! Got: " + str(type(params))
		raise Exception(msg)

def db_query_select(sql, params=None):
	"""Queries the database and returns a generator with the results.

	Args:
	mysql: The mysqldb database object.
	sql: The parameterized query.
	params: A tuple  the parameters for the query

	Returns:
	A list of objects

	"""

	check_params_type(params)
	conn = current_app.mysql.connection
	cur = conn.cursor()

	objects = []

	try:

		cur.execute(sql, params)

		if cur.description:
			cols = [col[0] for col in cur.description]
			for res in cur:
				serialized_res = [str(x) for x in res]
				objects.append(BaseObject(dict(zip(cols,serialized_res))))

	finally:
		cur.close()

	return objects

class BaseObject(dict):
	def __getattr__(self, key):
		if key in self:
			return self[key]
		else:
			try:
				return super(BaseObject, self).__getattr__(key)
			except:
				pass
		return None

# def protected(func):
# 	"""Decorator to enforce the presence of an oauth token.

# 	If a valid token is present, the request continues and this
# 	returns control to the decorated controller method. If
# 	no token is present or the token is invalid, this returns
# 	a failure response.

# 	"""

# 	@wraps(func)
# 	def decorated_function(*args, **kwargs):

# 		auth_token = request.headers.get('Authorization')
# 		decoded_token = decode_access_token(auth_token)
# 		user_id = decoded_token['user_id']

# 		print(user_id)

# 		sql = '''SELECT token, revoked, authenticated 
# 				 FROM user_access_token WHERE user_id=%s'''

# 		cur = current_app.mysql.connection.cursor()
# 		cur.execute(sql, (user_id,))
# 		res = cur.fetchone()

# 		expected_token = res[0]
# 		revoked 	   = res[1]
# 		authenticated  = res[2]
		
# 		if (auth_token == expected_token):

# 			# Possibly check token expiration
# 			g.user_id = decoded_token['user_id']

# 			return func(*args, **kwargs)

# 		return {'status':'Unauthorized.'}

# 	return decorated_function

# def check_params_type(params):
# 	"""Raises an exception if passed something besides a tuple"""

# 	if params and type(params) is not tuple:
# 		msg = "db_query_* functions require the params arg to be a tuple! Got: " + str(type(params))
# 		raise Exception(msg)

# def db_query_select(sql, params=None):
# 	"""Queries the database and returns a generator with the results.

# 	Args:
# 		mysql: The mysqldb database object.
# 		sql: The parameterized query.
# 		params: A tuple  the parameters for the query

# 	Returns:
# 		A list of objects

# 	"""

# 	check_params_type(params)
# 	conn = current_app.mysql.connection
# 	cur = conn.cursor()

# 	objects = []

# 	try:

# 		cur.execute(sql, params)

# 		if cur.description:
# 			cols = [col[0] for col in cur.description]
# 			for res in cur:
# 				serialized_res = [str(x) for x in res]
# 				objects.append(BaseObject(dict(zip(cols,serialized_res))))

# 	finally:
# 		cur.close()

# 	return objects


def db_query_insert(sql, params=None):
	"""Performs the provided insert query.

	Args:
		mysql: The mysqldb database object.
		sql: The parameterized query.
		params: A tuple the parameters for the query

	Returns:
		The number of affected rows.

	"""

	check_params_type(params)
	conn = current_app.mysql.connection
	cur = conn.cursor()

	rows_affected = 0

	try:
		cur.execute(sql, params)
		rows_affected = cur.rowcount

	# If we get an exception, don't return anything
	except IntegrityError as e:
		current_app.logger.error("Integrity Error: " + str(e))
	finally:
		cur.close()
		conn.commit()

	return rows_affected

# def db_query_update(sql, params=None):
# 	"""Performs the provided update query.

# 	Args:
# 		mysql: The mysqldb database object.
# 		sql: The parameterized query.
# 		params: A tuple the parameters for the query

# 	Returns:
# 		The number of affected rows.

# 	"""
# 	return db_query_insert(sql, params)

# def db_query_delete(sql, params=None):
# 	"""Performs the provided delete query.

# 	Args:
# 		mysql: The mysqldb database object.
# 		sql: The parameterized query.
# 		params: A tuple the parameters for the query

# 	Returns:
# 		The number of affected rows.

# 	"""
# 	return db_query_insert(sql, params)

# Returns a tuple with the coordinates for the bounding box
# Order: (lat_min, lat_max, lon_min, lon_max,)
# def bounding_box_for_coordinates(lat, lon):
# 	"""Generate the bounding box for a pair of coordinates.

# 	Args:
# 		lat (float): The latitude.
# 		lon (float): The longitude.

# 	Returns:
# 		tuple: A tuple with the bounding box (lat_min, lat_max, lon_min, lon_max)

# 	"""

# 	# Semi-axes of WGS-84 geoidal reference
# 	WGS84_a = 6378137.0  # Major semiaxis [m]
# 	WGS84_b = 6356752.3  # Minor semiaxis [m]

# 	# degrees to radians
# 	def deg2rad(degrees):
# 		return math.pi*degrees/180.0
# 	# radians to degrees
# 	def rad2deg(radians):
# 		return 180.0*radians/math.pi

# 	# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
# 	def WGS84EarthRadius(lat):
# 		# http://en.wikipedia.org/wiki/Earth_radius
# 		An = WGS84_a*WGS84_a * math.cos(lat)
# 		Bn = WGS84_b*WGS84_b * math.sin(lat)
# 		Ad = WGS84_a * math.cos(lat)
# 		Bd = WGS84_b * math.sin(lat)
# 		return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

# 	detection_radius_km = 1.609 * constants.DETECTION_RADIUS_MI
	
# 	lat = deg2rad(float(lat))
# 	lon = deg2rad(float(lon))
# 	box_radius = 1000*detection_radius_km

# 	# Radius of Earth at given latitude
# 	radius = WGS84EarthRadius(lat)
# 	# Radius of the parallel at given latitude
# 	pradius = radius*math.cos(lat)

# 	lat_min = rad2deg(lat - (box_radius/2)/radius)
# 	lat_max = rad2deg(lat + (box_radius/2)/radius)
# 	lon_min = rad2deg(lon - (box_radius/2)/pradius)
# 	lon_max = rad2deg(lon + (box_radius/2)/pradius)

# 	return (lat_min, lat_max, lon_min, lon_max,)

# def decode_access_token(token):
# 	"""Decodes a JWT.

# 	Args:
# 		token(str): The JSON Web Token.

# 	Returns:
# 		dict: The object decoded form the token.

# 	"""
# 	return jwt.decode(token, current_app.config['JWT_KEY'], algorithms=['HS256'])