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
    """This route send a message from authorised_user to the channel specified by channel_id,
    and return {message_id}"""
    data = request.get_json()
    result = message.message_send(
        data['token'],
        data['channel_id'],
        data['message']
    )
    return dumps({
        'message_id': result
    })

@APP.route("message/sendlater", methods=['POST'])
def http_message_sendlater():
    """This route send a message from authorised_user to the channel specified by
    channel_id automatically at a specified time in the future,
    and return {message_id}"""
    data = request.get_json()
    result = message.message_sendlater(
        data['token'],
        data['channel_id'],
        data['message'],
        data['time_sent']
    )
    return dumps({
        'message_id': result
    })

@APP.route("message/react", methods=['POST'])
def http_message_react():
    """This route get a message within a channel the authorised user is part of,
    add a "react" to that particular message and return nothing"""
    data = request.get_json()
    message.message_react(
        data['token'],
        data['message_id'],
        data['react_id']
    )
    return dumps({})

@APP.route("message/unreact", methods=['POST'])
def http_message_unreact():
    """This route get a message within a channel the authorised user is part of,
    remove a "react" to that particular message and return nothing"""
    data = request.get_json()
    message.message_unreact(
        data['token'],
        data['message_id'],
        data['react_id']
    )
    return dumps({})

@APP.route("message/pin", methods=['POST'])
def http_message_pin():
    """This route get a message within a channel, mark it as "pinned",
    and return nothing"""
    data = request.get_json()
    message.message_pin(
        data['token'],
        data['message_id']
    )
    return dumps({})

@APP.route("message/unpin", methods=['POST'])
def http_message_unpin():
    """This route get a message within a channel, remove it's mark as "pinned",
    and return nothing"""
    data = request.get_json()
    message.message_unpin(
        data['token'],
        data['message_id']
    )
    return dumps({})

@APP.route("message/remove", methods=['DELETE'])
def http_message_remove():
    """This route get a message_id for a message, this message is removed from the channel,
    and return nothing"""
    data = request.get_json()
    message.message_remove(
        data['token'],
        data['message_id']
    )
    return dumps({})

@APP.route("message/edit", methods=['PUT'])
def http_message_edit():
    """This route get a message, update it's text with new text.
    If the new message is an empty string, the message is deleted.
    And return nothing"""
    data = request.get_json()
    message.message_edit(
        data['token'],
        data['message_id'],
        data['message']
    )
    return dumps({})

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
