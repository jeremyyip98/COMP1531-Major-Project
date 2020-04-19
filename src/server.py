"""
UNSW COMP1531 Project Iteration 2
server.py
This file are running the frontend function works all the routes
"""
#pylint: disable= pointless-string-statement, invalid-name, trailing-whitespace
#some pointless string are put there incase we need it
import sys
from json import dumps
from threading import Thread, Timer
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
import auth
import channel
import channels
import message
import other
from image_upload import upload_profile_pic
from database import reset_message, restore_database
from pickle_it import pickle_it, database_update
from database import reset_message, restore_database, restore_channel_database
from standup import standup_start, standup_active, standup_send
from workspace_reset import workspace_reset
from helper_functions import create_admin

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

APP.config['UPLOAD_FOLDER'] = "profile_pictures"
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    '''example function by lecturer'''
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/imgurl/<string:filename>")
def show_profile_img(filename):
    return send_from_directory(APP.config['UPLOAD_FOLDER'], filename)


@APP.route("/channel/invite", methods=['POST'])
def http_invite():
    '''HTTP request for inviting someone to channel'''
    payload = request.get_json()
    channel.channel_invite(
        payload['token'],
        int(payload['channel_id']),
        int(payload['u_id']))
    return dumps({})

@APP.route("/channel/details", methods=['GET'])
def http_details():
    '''HTTP request for getting channel details'''
    details = channel.channel_details(
        request.args.get('token'),
        #need the int to convert from string to int
        int(request.args.get('channel_id')))
    return dumps(details)

@APP.route("/channel/messages", methods=['GET'])
def http_messages():
    '''HTTP request for getting messages of channel'''
    details = channel.channel_messages(
        request.args.get('token'),
        int(request.args.get('channel_id')),
        int(request.args.get('start')))
    return dumps(details)

@APP.route("/channels/list", methods=['GET'])
def http_list():
    '''HTTP route to list only channels the user can see'''
    token = request.args.get('token')
    details = channels.channels_list(token)
    return dumps(details)

@APP.route("/channels/listall", methods=['GET'])
def http_listall():
    '''Http route to list all the channels'''
    token = request.args.get('token')
    details = channels.channels_listall(token)
    return dumps(details)

@APP.route("/channels/create", methods=['POST'])
def http_create():
    '''HTTP route to create a channel'''
    payload = request.get_json()
    details = channels.channels_create(
        payload['token'],
        payload['name'],
        payload['is_public'])
    return dumps(details)

@APP.route("/channel/leave", methods=['POST'])
def http_leave():
    '''HTTP route to leave a channel'''
    payload = request.get_json()
    channel.channel_leave(
        payload['token'],
        int(payload['channel_id']))
    return dumps({})

@APP.route("/channel/join", methods=['POST'])
def http_join():
    '''HTTP route for user to join a channel'''
    payload = request.get_json()
    channel.channel_join(
        payload['token'],
        int(payload['channel_id']))
    return dumps({})

@APP.route("/channel/addowner", methods=['POST'])
def http_addowner():
    '''HTTP route for adding owner to a channel'''
    payload = request.get_json()
    channel.channel_addowner(
        payload['token'],
        int(payload['channel_id']),
        int(payload['u_id']))
    return dumps({})

@APP.route("/channel/removeowner", methods=['POST'])
def http_removeowner():
    '''HTTP route to remove an owner from a channel'''
    payload = request.get_json()
    channel.channel_removeowner(
        payload['token'],
        int(payload['channel_id']),
        int(payload['u_id']))
    return dumps({})

@APP.route("/auth/register", methods=['POST'])
def http_register():
    '''HTTP request for registering a user'''
    payload = request.get_json()
    details = auth.auth_register(
        payload['email'],
        payload['password'],
        payload['name_first'],
        payload['name_last'])
    return dumps(details)

@APP.route("/auth/login", methods=['POST'])
def http_login():
    '''HTTP request for logging in user'''
    payload = request.get_json()
    details = auth.auth_login(
        payload['email'],
        payload['password'])
    return dumps(details)

@APP.route("/auth/logout", methods=['POST'])
def http_logout():
    '''HTTP request for logging a user out'''
    payload = request.get_json()
    is_success = {"is_success" : auth.auth_logout(payload['token'])}
    return dumps(is_success)


@APP.route("/auth/passwordreset/request", methods=['POST'])
def httt_request_code():
    ''' HTTP request for requesting a password reset code '''
    payload = request.get_json()
    auth.auth_reset_password_request(payload['email'])
    return dumps({})

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def http_reset_password():
    ''' HTTP request for resetting password with a code '''
    payload = request.get_json()
    auth.auth_reset_password_reset(payload['reset_code'], payload['new_password'])
    return dumps({})


# Added code
@APP.route("/message/send", methods=['POST'])
def http_message_send():
    """This route send a message from authorised_user to the channel specified by channel_id,
    and return {message_id}"""
    data = request.get_json()
    result = message.message_send(
        data['token'],
        int(data['channel_id']),
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
        int(data['channel_id']),
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
        int(data['message_id']),
        int(data['react_id'])
    )
    return dumps({})

@APP.route("/message/unreact", methods=['POST'])
def http_message_unreact():
    """This route get a message within a channel the authorised user is part of,
    remove a "react" to that particular message and return nothing"""
    data = request.get_json()
    message.message_unreact(
        data['token'],
        int(data['message_id']),
        int(data['react_id'])
    )
    return dumps({})

@APP.route("/message/pin", methods=['POST'])
def http_message_pin():
    """This route get a message within a channel, mark it as "pinned",
    and return nothing"""
    data = request.get_json()
    message.message_pin(
        data['token'],
        int(data['message_id'])
    )
    return dumps({})

@APP.route("/message/unpin", methods=['POST'])
def http_message_unpin():
    """This route get a message within a channel, remove it's mark as "pinned",
    and return nothing"""
    data = request.get_json()
    message.message_unpin(
        data['token'],
        int(data['message_id'])
    )
    return dumps({})

@APP.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    """This route get a message_id for a message, this message is removed from the channel,
    and return nothing"""
    data = request.get_json()
    message.message_remove(
        data['token'],
        int(data['message_id'])
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
        int(data['message_id']),
        data['message']
    )
    return dumps({})

# Adding an extra route in order to reset the values in the list everytime I run the pytest
@APP.route("/message/reset", methods=['DELETE'])
def reset_store():
    """This function reset the list and returns nothing"""
    reset_message()
    restore_channel_database()
    restore_database()
    return dumps({})

@APP.route("/admin/userpermission/change", methods=['POST'])
def http_user_permission_change():
    """changes the Slackr Owner permission"""
    data = request.get_json()
    other.admin_userpermission_change(
        data['token'],
        int(data['u_id']),
        int(data['permission_id'])
    )
    return dumps({})

@APP.route("/admin/user/remove", methods=['POST'])
def http_admin_user_remove():
    '''Removes a user from Slackr and from any channel they are in'''
    data = request.get_json()
    other.admin_user_remove(
        data['token'],
        int(data['u_id'])
    )
    return dumps({})

@APP.route("/admin/create", methods=['POST'])
def http_admin_create():
    '''Helper function that creates an admin'''
    admin = create_admin()
    return dumps(admin)

@APP.route("/user/profile", methods=["GET"])
def http_profile():
    '''HTTP request for getting user info''' 
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return dumps(user_profile(token, u_id))

@APP.route("/user/profile/setname", methods=["PUT"])
def http_setname():
    '''HTTP request for changing a users name''' 
    payload = request.get_json()
    token = payload["token"]
    name_first = payload["name_first"]
    name_last = payload["name_last"]
    user_profile_setname(token, name_first, name_last)
    return dumps({})

@APP.route("/user/profile/setemail", methods=["PUT"])
def http_setemail():
    '''HTTP request for changing a user email'''
    payload = request.get_json()
    token = payload["token"]
    email = payload["email"]
    user_profile_setemail(token, email)
    return dumps({})

@APP.route("/user/profile/sethandle", methods=["PUT"])
def http_sethandle():
    '''HTTP request for changing a users handle name'''
    payload = request.get_json()
    token = payload["token"]
    handle_str = payload["handle_str"]
    user_profile_sethandle(token, handle_str)
    return dumps({})

@APP.route("/user/profile/uploadphoto", methods=["POST"])
def http_upload_photo():
    payload = request.get_json()
    token = payload["token"]
    img_url = payload["img_url"]
    x_start = int(payload["x_start"])
    y_start = int(payload["y_start"])
    x_end = int(payload["x_end"])
    y_end = int(payload["y_end"]) 
    """ This possibly should involve threading incase it slows down whole server """
    upload_profile_pic(token, img_url, x_start, y_start, x_end, y_end)
    print("HERE")
    return dumps({})

@APP.route("/users/all", methods=['GET'])
def http_users_all():
    '''A helper function to get data on all user'''
    token = request.args.get('token')
    return dumps(other.users_all(token))

@APP.route("/search", methods=['GET'])
def http_search():
    '''HTTP request for searching for information'''
    token = request.args.get('token', None)
    print(token)
    query_str = request.args.get('query_str', None)
    return dumps(other.search(token, query_str))

@APP.route("/standup/start", methods=["POST"])
def http_standup_start():
    '''HTTP request to start standup'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    length = payload['length']
    result = standup_start(token, channel_id, length)
    return dumps(result)

@APP.route("/standup/active", methods=["GET"])
def http_standup_active():
    '''HTTP request for activating standup'''
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    result = standup_active(token, channel_id)
    return dumps(result)

@APP.route("/standup/send", methods=["POST"])
def http_standup_send():
    '''HTTP request for sending message for standup'''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    msg = payload['message']
    standup_send(token, channel_id, msg)
    return dumps({})

@APP.route("/workspace/reset", methods=["POST"])
def http_workspace_reset():
    '''HTTP request for reseting all the data in database'''
    workspace_reset()
    return dumps({})

@APP.after_request
def pickle_store(response):
    '''HTTP request for pickling data after every request'''
    timer = Timer(1.5, pickle_it)
    timer.daemon = True
    timer.start()
    return response

if __name__ == "__main__":
    UPDATE = Thread(target=database_update)
    UPDATE.start()
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8081), debug=True)
