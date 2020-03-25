import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import error
import auth

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/auth/register", methods=['PUT'])
def http_register():
    payload = request.get_json()
    details = auth.auth_register(
        payload['email'],
        payload['password'],
        payload['name_first'],
        payload['name_last'])
    return dumps(details)


if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080), debug=True)
