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

# Possible routes for message/send (Working in progress)
@APP.route("/message/send", methods=['POST'])
def message_send():
    messages = get_message()
    if not messages:    # If messages is empty
        message_id = 0
    else:
        most_recent_message = messages[-1]
        message_id = 


    data = request.get_json()
    messages.append(data)
    return dumps({})

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
