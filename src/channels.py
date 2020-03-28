"""
UNSW COMP1531 Iteration 2
channel.py
Written by Jackie Cai z5259449
"""
from database import channel_ids, list_of_channels, search_database, get_u_id
from error import AccessError, InputError

def generate_channel_id():
    """Makes a channel id and adds it to the databse"""
    channel_id = max(channel_ids)
    channel_id += 1
    channel_ids.append(channel_id)
    return channel_id
def channels_create(token, name, is_public):
    """Makes a channel with a name and sets it as public or not then it makes the
    person with the token the owner and first member of the channel"""
    #Check for access error first
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    user = get_u_id(token)
    if len(name) > 20:
        raise InputError(description='Channel Name Too Long')
    re_channel_id = generate_channel_id()
    new_channel = {
        'channel_id' : re_channel_id,
        'channel_name' : name,
        'is_public' : is_public,
        'owner_members' : [user],
        'all_members' : [user],
    }
    list_of_channels['channels'].append(new_channel)
    return re_channel_id
def channels_list(token):
    """Gets a token and returns a list of channel the user is in"""
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    #make a list to store all channels user is in
    authed_channel = []
    #get the user's id
    user = get_u_id(token)
    #iterate through the list of channels
    for chan in list_of_channels['channels']:
        #iterate through list of members
        for mem in chan['all_members']:
            #if user are in the channel append to list
            if mem == user:
                add = {
                    'channel_id' : chan['channel_id'],
                    'channel_name' : chan['channel_name']
                }
                authed_channel.append(add)
    return authed_channel
def channels_listall(token):
    """Gets a token and returns a list of channel that exist"""
    #check for access error
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    #no access error means they are user and returns all channels
    authed_channel = []
    for chan in list_of_channels['channels']:
        add = {
            'channel_id' : chan['channel_id'],
            'channel_name' : chan['channel_name']
        }
        authed_channel.append(add)
    return authed_channel
