from enum import Enum

class Status(Enum):

	# Success
	SUCCESS = (20000, "Success")

	# Bad Request
	MISSING_PARAMETERS = (40000, "Missing required parameters")

	# Unauthorized
	INVALID_TOKEN	= (40100, "Unauthorized.")
	MISSING_API_KEY = (40101, "Unauthorized.")

	# Server Errors

	def __init__(self, code, message):
		self.code = code
		self.message = message

	@classmethod
	def success(e):
		return e.SUCCESS