import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import message

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

# Added code
@APP.route("message/send", methods=['POST'])
def http_message_send():
    """This function send a message from authorised_user to the channel specified by channel_id,
    and returns {message_id}"""
    message = 


@APP.route("message/sendlater", methods=['POST'])
def http_message_sendlater():
    pass

@APP.route("message/react", methods=['POST'])
def http_message_react():
    pass

@APP.route("message/unreact", methods=['POST'])
def http_message_unreact():
    pass

@APP.route("message/pin", methods=['POST'])
def http_message_pin():
    pass

@APP.route("message/unpin", methods=['POST'])
def http_message_unpin():
    pass

@APP.route("message/remove", methods=['DELETE'])
def http_message_remove():
    pass

@APP.route("message/edit", methods=['PUT'])
def http_message_edit():
    pass

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
