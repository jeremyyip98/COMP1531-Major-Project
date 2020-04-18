""" File includes implementation for search, users_all and admin permission change """
from database import check_token, get_all_users, registered_users_store,\
    search_database, get_message, get_permission, get_profile_allinfo, list_of_channels
from error import AccessError, InputError
#pylint: disable = line-too-long
#last line to delete user needs list comprehension which is a long line since
#registered_user_store['registered_user'] is repeated twice which makes a ling line
# Probably should need permission to do this!!!

def users_all(token):
    """ Returns the users dictionry type with details of every registered user """
    check_token(token)
    return {"users" : get_all_users()}

def search(token, query_str):
    """ Given a query string and token will return a list of messages that contain the term """
    check_token(token)
    query_str_matches = []
    messages = get_message()
    for message in messages:
        if query_str in message['message']:
            query_str_matches.append(message)
    query_str_matches = sorted(query_str_matches, key=lambda i: i['time_created'], reverse=True)
    return {"messages" : query_str_matches}


def admin_userpermission_change(token, u_id, permission_id):
    """Given a admin token you can change the permission ID of another user"""
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    #this functions raises an input error if the u_id does not refer to valid user
    user = get_profile_allinfo(u_id)
    a_user = get_permission(token)
    if permission_id not in (1, 2):
        raise InputError(description='Not valid permission id')
    if a_user != 1:
        raise AccessError(description='Not an Owner of Slackr')
    user['permission_id'] = permission_id

def admin_user_remove(token, u_id):
    """Given an admin token you an remove another user from slackr"""
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    #this functions raises an input error if the u_id does not refer to valid user
    get_profile_allinfo(u_id)
    a_user = get_permission(token)
    if a_user != 1:
        raise AccessError(description='Not an Owner of Slackr')
    # iterate through the channel and find if the user is in any of them
    for channel in list_of_channels:
        if u_id in channel['all_members']:
            channel['all_members'].remove(u_id)
            if u_id in channel['owner_members']:
                channel['owner_members'].remove(u_id)
    registered_users_store['registered_users'] = [i for i in registered_users_store['registered_users'] if not i['u_id'] == u_id]
