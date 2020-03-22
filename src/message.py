"""
UNSW COMP1531 Project Iteration 2
message.py
Written by: Yip Jeremy Chung Lum, z5098112
"""
from database import get_message, get_react
from auth import auth_register, auth_login, auth_logout
from channels import channels_create, channels_list
from channel import channel_join, channel_addowner, channel_messages
from error import InputError, AccessError
from datetime import datetime


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
        "reacts" : [{           # When the message is creating, no one should be able to react to it
            
        }],
        "is_pinned" : False     # When the message is creating, no one should be able to pin it
    }
    message.append(dictionary)
    return message

def react_create(u_id, is_this_user_reacted):
    react = get_react()


def message_send(token, channel_id, message):
    joined = False
    for dict_item in channels_list(token):      # channels_list() return a list of all channels (a list of dictionaries) that the authorised user is part of
                                                # Hence loop through the dictionaries
        for key in dict_item:                   # Loop through the key in the dictionaries
            if channel_id == key[channel_id]:   # If the given channel_id exists
                joined = True
                break
    if len(message) > 1000:
        raise InputError('Message must be less than or equal 1000 characters')
    elif joined is False:
         raise AccessError('Authorised user has not joined the channel')

    message = message_create(channel_id, get_u_id(token), message, datetime.now()) # Assume get_u_id(token) has already been implemented in datebase.py 
    return message[-1]['message_id']
    
def message_sendlater(token, channel_id, message, time_sent):
    pass

def message_react(token, message_id, react_id):
    pass

def message_unreact(token, message_id, react_id):
    pass

def message_pin(token, message_id):
    pass

def message_unpin(token, message_id):
    pass

def message_remove(token, message_id):
    pass

def message_edit(token, message_id, message):
    pass