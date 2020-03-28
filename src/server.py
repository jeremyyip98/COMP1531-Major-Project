"""
UNSW COMP1531 Project Iteration 2
server.py
This file are running the frontend function works all the routes
"""
import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import error
import auth
import channel
import channels
import message

def defaultHandler(err):
    """A given function by instructors"""
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
    
@APP.route("/channel/invite", methods=['POST'])
def http_invite():
    data = request.get_json()
    channels.channel_invite(
        payload['token'],
        payload['channel_id'],
        payload['u_id'])
    return dumps({})
    
@APP.route("/channel/details", methods=['GET'])
def http_details():
    details = channels.channel_details(
        request.args.get('token'),
        request.args.get('channel_id'))
        
    return dumps(details)
    
@APP.route("/channel/messages", methods=['GET'])
def http_messages():
    details = channels.channel_messages(
        request.args.get('token'),
        request.args.get('channel_id'),
        request.args.get('start'))
        
    return dumps(details)

@APP.route("/channels/list", methods=['GET'])
def http_list():
    payload = request.get_json()
    details = channels.channels_list(
        payload['token']
    )
    return(
        {
            'channels' : details
        }
    )

@APP.route("/channels/listall", methods=['GET'])
def http_listall():
    payload = request.get_json()
    details = channels.channels_listall(
        payload['token']
    )
    return(
        {
            'channels' : details
        }
    )

@APP.route("/channels/create", methods=['POST'])
def http_create():
    payload = request.get_json()
    details = channels.channels_create(
        payload['token'],
        payload['channel_name'],
        payload['is_public'])
    return(
        {
            'channel_id' : details
        }
    )

@APP.route("/channel/leave", methods=['POST'])
def http_leave():
    payload = request.get_json()
    channel.channel_leave(
        payload['token'],
        payload['channel_id']
    )
    return dumps({})

@APP.route("/channel/join", methods=['POST'])
def http_join():
    payload = request.get_json()
    channel.channel_join(
        payload['token'],
        payload['channel_id']
    )
    return dumps({})

@APP.route("/channel/addowner", methods=['POST'])
def http_addowner():
    payload = request.get_json()
    channel.channel_addowner(
        payload['token'],
        payload['channel_id'],
        payload['u_id']
    )
    return dumps({})

@APP.route("/channel/removeowner", methods=['POST'])
def http_removeowner():
    payload = request.get_json()
    channel.channel_leave(
        payload['token'],
        payload['channel_id']
    )
    return dumps({})

@APP.route("/auth/register", methods=['POST'])
def http_register():
    payload = request.get_json()
    details = auth.auth_register(
        payload['email'],
        payload['password'],
        payload['name_first'],
        payload['name_last'])
    return dumps(details)

@APP.route("/auth/login", methods=['POST'])
def http_login():
    payload = request.get_json()
    details = auth.auth_login(
        payload['email'],
        payload['password'])
    return dumps(details)

@APP.route("/auth/logout", methods=['POST'])
def http_logout():
    payload = request.get_json()
    is_success = {"is_sucess" : auth.auth_logout(payload['token'])}
    return dumps(is_success)


# Added code
@APP.route("/message/send", methods=['POST'])
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

@APP.route("/message/sendlater", methods=['POST'])
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

@APP.route("/message/react", methods=['POST'])
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

@APP.route("/message/unreact", methods=['POST'])
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

@APP.route("/message/pin", methods=['POST'])
def http_message_pin():
    """This route get a message within a channel, mark it as "pinned",
    and return nothing"""
    data = request.get_json()
    message.message_pin(
        data['token'],
        data['message_id']
    )
    return dumps({})

@APP.route("/message/unpin", methods=['POST'])
def http_message_unpin():
    """This route get a message within a channel, remove it's mark as "pinned",
    and return nothing"""
    data = request.get_json()
    message.message_unpin(
        data['token'],
        data['message_id']
    )
    return dumps({})

@APP.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    """This route get a message_id for a message, this message is removed from the channel,
    and return nothing"""
    data = request.get_json()
    message.message_remove(
        data['token'],
        data['message_id']
    )
    return dumps({})

@APP.route("/message/edit", methods=['PUT'])
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
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080),debug=True)
