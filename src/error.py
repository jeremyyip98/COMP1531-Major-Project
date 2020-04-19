"""
error.py
"""
from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    """Return access error"""
    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    """Return input error"""
    code = 400
    message = 'No message specified'