"""
UNSW COMP1531 Project Iteration 2
message.py
Written by: Yip Jeremy Chung Lum, z5098112
"""
from datetime import datetime
from database import get_message, get_u_id
from auth import auth_register, auth_login, auth_logout
from channels import channels_create, channels_list, channels_listall
from channel import channel_join, channel_addowner, channel_messages
from error import InputError, AccessError


def message_create(channel_id, u_id, message, time):
    """This function create a message and returns it"""
    message = get_message()
    if not message:    # If messages is empty
        message_id = 0
    else:
        most_recent_message = message[-1]
        message_id = most_recent_message['message_id'] + 1

    dictionary = {
        "channel_id" : channel_id,
        "message_id" : message_id,
        "u_id" : u_id,
        "message" : message,
        "time_created" : time,
        "reacts" : [{          # When the message is creating, no one should be able to react to it
            'react_id' : 1,
            'u_ids' : [],
            'is_this_user_reacted' : False
        }],
        "is_pinned" : False     # When the message is creating, no one should be able to pin it
    }
    message.append(dictionary)
    return message

# Helper function for message_send and message_sendlater
def check_joined_channel(token, channel_id):
    """This function check has the authorised user joined the channel or not
    returns true or false"""
    joined = False
    for dict_item in channels_list(token):      # channels_list() return a list of all channels (a list of dictionaries) that the authorised user is part of
                                                # Hence loop through the dictionaries
        for key in dict_item:                   # Loop through the key in the dictionaries
            if channel_id == key[channel_id]:   # If the given channel_id exists
                joined = True
                break
    return joined

# Helper function for check_react and check_unreact
def check_valid_message(u_id, message_id):
    """This function check is the message_id valid or not
    returns true or false"""
    message = get_message()
    valid_message = False

    for dict_item in message:
        if u_id == dict_item['u_id']:
            if message_id == dict_item['message_id']:
                valid_message = True
                break
    return valid_message

def check_same_react_id(react, react_id, u_id):
    """This function check has the user already been reacted with the same react_id before"""
    joined = False
    for dict_item in react:
        if react_id == dict_item['react_id']:
            for id in dict_item['u_ids']:
                if u_id == id:
                    joined = True
                    break
    return joined

def check_message_contains_react(message_id, react_id):
    """This function check has message_id already contains an active React
    with ID react_id and return true or false"""
    message = get_message()
    for dict_message in message:
        if message_id == dict_message['message_id']:
            react = dict_message['reacts']
            joined = False
            for dict_item in react:
                if react_id == dict_item['react_id']:
                    joined = True
                    break
    return joined

def react_create(react_id, u_id, message_id):
    """This functions create a react and returns nothing"""
    message = get_message()
    # Loop through the list until it reaches the correct message
    for dict_message in message:
        if message_id == dict_message['message_id']:
            react = dict_message['reacts']

            # Checking if the user has already reacted with the same react_id before
            joined = check_same_react_id(react, react_id, u_id)
            # Only add the user to u_ids, when he has not reacted before
            if joined is False:
                react['u_ids'].append(u_id)
            # If the authorised user is reacting to his/her own message
            if u_id == dict_message['u_id']:
                react['is_this_user_reacted'] = False    # No need to loop through the list of dict, since the spec
                                                        # has specified that the only valid React ID the front end has is 1
                                                        # Which there should be only 1 React Id in every messages

def react_remove(react_id, u_id, message_id):
    """This functions remove a react and returns nothing"""
    message = get_message()
    # Loop through the list until it reaches the correct message
    for dict_message in message:
        if message_id == dict_message['message_id']:
            react = dict_message['reacts']

            # Checking if the user has already reacted with the same react_id before
            joined = check_same_react_id(react, react_id, u_id)
            # Only remove the user to u_ids, when he has reacted before
            if joined is True:
                react['u_ids'].remove(u_id)
            # If the authorised user is removing the reacte to his/her own message
            if u_id == dict_message['u_id']:
                react['is_this_user_reacted'] = False    # No need to loop through the list of dict, since the spec
                                                        # has specified that the only valid React ID the front end has is 1
                                                        # Which there should be only 1 React Id in every messages
def message_send(token, channel_id, message):
    """This function send a message from authorised_user to the channel specified by channel_id"""
    joined = check_joined_channel(token, channel_id)

    if len(message) > 1000:
        raise InputError('Message must be less than or equal 1000 characters')
    if joined is False:
        raise AccessError('Authorised user has not joined the channel')

    message = message_create(channel_id, get_u_id(token), message, datetime.now())
    return message[-1]['message_id']

def message_sendlater(token, channel_id, message, time_sent):
    """This function send a message from authorised_user to the channel specified by channel_id automatically at a specified time in the future"""
    joined = check_joined_channel(token, channel_id)

    if not any(dict['channel_id'] == channel_id for dict in channels_listall(token)):   # if channel_id is not a valid channel
        raise InputError('Channel ID has to be a valid channel')
    if len(message) > 1000:
        raise InputError('Message must be less than or equal 1000 characters')
    if time_sent < datetime.now():    # If time_sent is a time in the past
        raise InputError('Time has to be a future time')
    if joined is False:
        raise AccessError('Authorised user has not joined the channel')

    message = message_create(channel_id, get_u_id(token), message, time_sent)
    return message[-1]['message_id']

def message_react(token, message_id, react_id):
    """This function given a message within a channel the authorised user is part of,
    add a "react" to that particular message"""
    valid_message = check_valid_message(get_u_id(token), message_id)

    if valid_message is False:
        raise InputError('Message_id has to be a valid message')
    if react_id != 1:
        raise InputError('React_id has to be a valid react ID')
    joined = check_message_contains_react(message_id, react_id)
    if joined is True:
        raise InputError('Message already contains the given react_id')

    react_create(react_id, get_u_id(token), message_id)

def message_unreact(token, message_id, react_id):
    """This function given a message within a channel the authorised user is part of,
    remove a "react" to that particular message"""
    valid_message = check_valid_message(get_u_id(token), message_id)

    if valid_message is False:
        raise InputError('Message_id has to be a valid message')
    if react_id != 1:
        raise InputError('React_id has to be a valid react ID')
    joined = check_message_contains_react(message_id, react_id)
    if joined is False:
        raise InputError('Message does not contains the given react_id')

    react_remove(react_id, get_u_id(token), message_id)

def message_pin(token, message_id):
    pass

def message_unpin(token, message_id):
    pass

def message_remove(token, message_id):
    pass

def message_edit(token, message_id, message):
    pass