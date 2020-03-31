from database import check_token, get_all_users, get_profile,\
    search_database, get_message, get_permission, get_profile_allinfo, check_user_in_channel
from message import get_channel_id
from error import AccessError, InputError

# Probably should need permission to do this!!!

def users_all(token):
    check_token(token)
    return {"users" : get_all_users()}

def search(token, query_str):
    check_token(token)
    query_str_matches = []
    messages = get_message()
    for message in messages:
        if query_str in message['message']:
            query_str_matches.append(message)
    query_str_matches =  sorted(query_str_matches, key = lambda i: i['time_created'], reverse=True)
    return {"messages" : query_str_matches}

def standup_start():
    pass

def admin_userpermission_change(token, u_id, permission_id):
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
    