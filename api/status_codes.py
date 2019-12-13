from enum import Enum

class Status(Enum):

	# Success
	SUCCESS = (200, "Success")
	EMPTY_SET = (200, "Empty Set")

	# Bad Request
	MISSING_PARAMETERS = (400, "Missing required parameters")

	# Unknown
	REGISTRATION_FAILED = (422, "Registration Failed")
	BAD_PASSWORD = (422,"Bad Password")
	INVALID_USERNAME = (422,"Invalid Username")

	# Unauthorized
	INVALID_TOKEN	= (401, "Unauthorized.")
	MISSING_API_KEY = (401, "Unauthorized.")

	# Server Errors

	def __init__(self, code, message):
		self.code = code
		self.message = message

	@classmethod
	def success(e):
		return e.SUCCESS