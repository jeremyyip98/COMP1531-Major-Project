import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

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

@APP.route("/channels/list", methods=['GET'])
def http_list():
    pass

@APP.route("/channels/listall", methods=['GET'])
def http_listall():
    pass

@APP.route("/channels/create", methods=['GET'])
def http_create():
    pass

@APP.route("/channel/leave", methods=['POST'])
def http_leave():
    pass

@APP.route("/channel/join", methods=['POST'])
def http_join():
    pass

@APP.route("/channel/addowner", methods=['POST'])
def http_addowner():
    pass
@APP.route("/channel/removeowner", methods=['POST'])
def http_removeowner():
    pass

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
