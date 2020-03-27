"""
UNSW COMP1531 Project Iteration 2
message.py
Written by: Yip Jeremy Chung Lum, z5098112
"""
from datetime import datetime
from database import get_message, get_u_id, get_channel
from channels import  channels_list, channels_listall
from channel import channel_details
from error import InputError, AccessError

##############################################################
# Helper functions for the functions of HTTP Routes of Message
##############################################################
# Helper function for message_send() and message_sendlater()
def message_create(channel_id, u_id, message, time):
    """This function create a message and return it"""
    message = get_message()
    if message == [{}]:    # If messages is empty
        message_id = 0
    else:
        most_recent_message = message[-1]
        message_id = most_recent_message['message_id'] + 1

    dictionary = {
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

    # Add the message to it's corresponding channel
    channel_add(channel_id, message_id)

    return message

# Helper function for message_create() and get_channel_id()
def channel_add(channel_id, message_id):
    """This function store a list of dictionaries containing
    the channel_id with it's corresponding message_ids and return nothing"""
    channel = get_channel()
    if not channel: # If the channel is empty
        dictionary = {
            "channel_id" : channel_id,
            "channel_messages" : [message_id]
        }
        channel.append(dictionary)
    else:
        for dict_channel in channel:
            if dict_channel['channel_id'] == channel_id:
                dict_channel['channel_messages'].append(message_id)

# Helper function for message_send() and message_sendlater()
def check_joined_channel(token, channel_id):
    """This function check has the authorised user joined the channel or not
    return true or false"""
    joined = False

    # channels_list() return a list of all channels (a list of dictionaries)
    # that the authorised user is part of, hence loop through the dictionaries
    for dict_item in channels_list(token):
        if dict_item['channel_id'] == channel_id:   # If the given channel_id exists
            joined = True
            break
    return joined

# Helper function for react_create and react_remove
def check_same_react_id(react, react_id, u_id):
    """This function check has the user already been reacted with the same react_id before"""
    joined = False
    for dict_item in react:
        if dict_item['react_id'] == react_id:
            for id_list in dict_item['u_ids']:
                if id_list == u_id:
                    joined = True
                    break
    return joined

# Helper function for message_react() and message_unreact()
def check_valid_message(u_id, message_id):
    """This function check is the message_id valid or not
    return true or false"""
    message = get_message()
    valid_message = False

    for dict_item in message:
        if dict_item['u_id'] == u_id:
            if dict_item['message_id'] == message_id:
                valid_message = True
                break
    return valid_message

# Helper function for message_react and message_unreact
def check_message_contains_react(message_id, react_id):
    """This function check has message_id already contains an active React
    with ID react_id and return true or false"""
    message = get_message()
    for dict_message in message:
        if dict_message['message_id'] == message_id:
            react = dict_message['reacts']
            joined = False
            for dict_item in react:
                if dict_item['react_id'] == react_id:
                    joined = True
                    break
    return joined

# Helper function for message_react()
def react_create(react_id, u_id, message_id):
    """This functions create a react and return nothing"""
    message = get_message()
    # Loop through the list until it reaches the correct message
    for dict_message in message:
        if dict_message['message_id'] == message_id:
            react = dict_message['reacts']

            # Checking if the user has already reacted with the same react_id before
            joined = check_same_react_id(react, react_id, u_id)
            # Only add the user to u_ids, when he has not reacted before
            if joined is False:
                react['u_ids'].append(u_id)
            # If the authorised user is reacting to his/her own message
            if dict_message['u_id'] == u_id:
                react['is_this_user_reacted'] = False
                # No need to loop through the list of dict, since the spec
                # has specified that the only valid React ID the front end has is 1
                # Which there should be only 1 React Id in every messages

# Helper function for message_unreact()
def react_remove(react_id, u_id, message_id):
    """This functions remove a react and return nothing"""
    message = get_message()
    # Loop through the list until it reaches the correct message
    for dict_message in message:
        if dict_message['message_id'] == message_id:
            react = dict_message['reacts']

            # Checking if the user has already reacted with the same react_id before
            joined = check_same_react_id(react, react_id, u_id)
            # Only remove the user to u_ids, when he has reacted before
            if joined is True:
                react['u_ids'].remove(u_id)
            # If the authorised user is removing the reacte to his/her own message
            if dict_message['u_id'] == u_id:
                react['is_this_user_reacted'] = False
                # No need to loop through the list of dict, since the spec
                # has specified that the only valid React ID the front end has is 1
                # Which there should be only 1 React Id in every messages

# Helper function for check_owner(), message_pin() and messagge_unpin()
def get_channel_id(message_id):
    """This function given message_id, search through message,
    and return the channel_id corresponding to the message_id"""
    channel = get_channel()

    for dict_channel in channel:
        if message_id in dict_channel['channel_messages']:
            channel_id = dict_channel['channel_id']

    return channel_id

# Helper function for message_pin() and message_unpin()
def check_owner(token, message_id):
    """This function check is the authorised user an owner or not,
    return true or false"""
    is_owner = False
    u_id = get_u_id(token)
    channel_id = get_channel_id(message_id)
    owners_list = channel_details(token, channel_id)

    for dict_owner in owners_list:
        if dict_owner['u_id'] == u_id:
            is_owner = True
            break
    return is_owner

# Helper function for message_pin() and message_unpin()
def check_pinned(message_id):
    """This function check is Message with ID message_id already pinned or not,
    return true or false"""
    message = get_message()
    pinned = False

    for dict_message in message:
        if dict_message['message_id'] == message_id:
            if dict_message['is_pinned'] is True:
                pinned = True
                break
    return pinned
# Helper function for message_pin()
def pin_add(message_id):
    """This function pin a message and return nothing"""
    message = get_message()
    for dict_message in message:
        if dict_message['message_id'] == message_id:
            dict_message['is_pinned'] = True

# Helper function for message_unpin()
def pin_remove(message_id):
    """This function unpin a message and return nothing"""
    message = get_message()
    for dict_message in message:
        if dict_message['message_id'] == message_id:
            dict_message['is_pinned'] = False

# Helper function for message_remove()
def is_user_sent_message(token, message_id):
    """This function check if message with message_id was sent by
    the authorised user making this request, and return true or false"""
    is_user_sent = False
    u_id = get_u_id(token)
    message = get_message()

    for dict_message in message:
        if dict_message['message_id'] == message_id:
            if dict_message['u_id'] == u_id:
                is_user_sent = True
                break
    return is_user_sent

##############################################################
# Functions of HTTP Routes of Message
##############################################################
def message_send(token, channel_id, message):
    """This function send a message from authorised_user to the channel specified by channel_id
    and return the message_id"""
    joined = check_joined_channel(token, channel_id)

    if len(message) > 1000:
        raise InputError('Message must be less than or equal 1000 characters')
    if joined is False:
        raise AccessError('Authorised user has not joined the channel')

    message = message_create(channel_id, get_u_id(token), message, datetime.now())
    return message[-1]['message_id']

def message_sendlater(token, channel_id, message, time_sent):
    """This function send a message from authorised_user to the channel specified by
    channel_id automatically at a specified time in the future,
    and return the message_id"""
    joined = check_joined_channel(token, channel_id)

    # if channel_id is not a valid channel
    if not any(dict['channel_id'] == channel_id for dict in channels_listall(token)):
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
    add a "react" to that particular message and return nothing"""
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
    remove a "react" to that particular message and return nothing"""
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
    """This function given a message within a channel, mark it as "pinned",
    and return nothing"""
    valid_message = check_valid_message(get_u_id(token), message_id)

    if valid_message is False:
        raise InputError('Message_id has to be a valid message')

    is_owner = check_owner(token, message_id)
    if is_owner is False:
        raise InputError('The authorised user has to be an owner')

    is_pinned = check_pinned(message_id)
    if is_pinned is True:
        raise InputError('The message is already pinned')

    channel_id = get_channel_id(message_id)
    joined = check_joined_channel(token, channel_id)
    if joined is False:
        raise AccessError('Authorised user is not a member of the channel')

    pin_add(message_id)

def message_unpin(token, message_id):
    """This function given a message within a channel, remove it's mark as "pinned",
    and return nothing"""
    valid_message = check_valid_message(get_u_id(token), message_id)

    if valid_message is False:
        raise InputError('Message_id has to be a valid message')

    is_owner = check_owner(token, message_id)
    if is_owner is False:
        raise InputError('The authorised user has to be an owner')

    is_pinned = check_pinned(message_id)
    if is_pinned is False:
        raise InputError('The message is already unpinned')

    channel_id = get_channel_id(message_id)
    joined = check_joined_channel(token, channel_id)
    if joined is False:
        raise AccessError('Authorised user is not a member of the channel')

    pin_remove(message_id)

def message_remove(token, message_id):
    """This function given a message_id for a message, this message is removed from the channel,
    and return nothing"""
    valid_message = check_valid_message(get_u_id(token), message_id)

    if valid_message is False:
        raise InputError('Message_id no longer exist')

    is_user_sent = is_user_sent_message(token, message_id)
    is_owner = check_owner(token, message_id)

    # Currently only checked is the user an owner of the channel
    # Haven't include the case when user is an owner of slackr (Don't know where to get this info.)
    if is_user_sent is False or is_owner is False:
        raise AccessError('The authorised user is not the one who sent the message, nor an owner.')

    message = get_message()
    for dict_message in message:
        if dict_message['message_id'] == message_id:
            del dict_message
            break

def message_edit(token, message_id, message):
    """This function given a message, update it's text with new text.
    If the new message is an empty string, the message is deleted.
    And return nothing"""
    valid_message = check_valid_message(get_u_id(token), message_id)

    if valid_message is False:
        raise InputError('Message_id no longer exist')

    is_user_sent = is_user_sent_message(token, message_id)
    is_owner = check_owner(token, message_id)

    # Currently only checked is the user an owner of the channel
    # Haven't include the case when user is an owner of slackr (Don't know where to get this info.)
    if is_user_sent is False or is_owner is False:
        raise AccessError('The authorised user is not the one who sent the message, nor an owner')

    message = get_message()
    for dict_message in message:
        if dict_message['message_id'] == message_id:
            if not message_id:  # If it's an empty string
                message_remove(token, message_id)
            else:
                dict_message['message'] = message
