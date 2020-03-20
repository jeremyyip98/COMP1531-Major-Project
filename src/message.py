from auth import auth_register, auth_login, auth_logout
from channels import channels_create, channels_list
from channel import channel_join, channel_addowner, channel_messages
from error import InputError, AccessError

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