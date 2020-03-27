import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import error
import auth
import channel
import channels

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

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080), debug=True)
