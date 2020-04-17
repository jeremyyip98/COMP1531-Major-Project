from error import AccessError, InputError
from datetime import datetime, timezone

u_ids = [0]

registered_users_store = {
                            'registered_users' : 
                                [
                                  #  {   
                                  # 'u_id' : 0,
                                  # 'email' : example_email,
                                  # 'name_first' : Firs,
                                  # 'name_last' : Last,
                                  # 'hash' : encrypted password,
                                  # 'token' : token,
                                  # 'handle_str' :firstlast
                                  # 'permission_id': 1/2             
                                  #  }    
                                ]

                        }

channel_ids = [0]

list_of_channels = [#{
                      #'channel_id' : channel_id,
                      #'channel_name' : channel_name
                      #'is_public' : boolean
                      #'owner_members' : [u_id] (list of owner u_ids)
                      #'all_members : [u_id] (list of member u_ids)
                      #'is_in_standup: False
                      #'standup_finish_time: time
                      #'channel_messages : [] (list of message_id (int))
                      # }
]

def get_data():
    return registered_users_store
    
def restore_database():
    global registered_users_store
    registered_users_store.clear()
    registered_users_store = {
                            'registered_users' : 
                                [
                                  #  {                   
                                  #  }    
                                ]

                        }
    return

def restore_channel_database():
    """reseting the channel database to clear it"""
    global list_of_channels
    list_of_channels.clear()
    global channel_ids
    channel_ids.clear()
    channel_ids.append(0)

message_list = [
    # {
    # message_id (int)
    # u_id (int)
    # message (string)
    # time_created (integer (unix timestamp))
    # reacts (list of dictionaries)
    # is_pinned (Boolean)
    # }
]

standup_queue = []
def restore_standup_queue():
    global standup_queue
    standup_queue.clear()

def check_token(token):
    """ Takes token raises Access Error if the token is not linked to any user,
        otherwise it returns True """
    if search_database(token) is False:
        raise AccessError
    else:
        return True

def get_u_id(token):
    """ Takes token and returns the u_id of user token belongs to"""
    return search_database(token)['u_id']

def get_permission(token):
    return search_database(token)['permission_id']

def get_email(token):
    """ Takes token and returns the email of user token belongs to"""
    return search_database(token)['email']

def get_formatted_user(token):
    """ Returns a user dictionary in the spec format """
    user = search_database(token)
    formatted_user = {}
    formatted_user['u_id'] = user['u_id']
    formatted_user['email'] = user['email']    
    formatted_user['name_first'] = user['name_first']  
    formatted_user['name_last'] = user['name_last']  
    formatted_user['handle_str'] = user['handle_str']
    formatted_user['permission_id'] = user['permission_id']
    return formatted_user  

def get_all_users():
    """ Returns the users type from the spec """
    users = []
    for user in registered_users_store['registered_users']:
        users.append(get_formatted_user(user['token']))
    return users


def search_database(token):

    """ Takes token and returns all information of its registered user in a dictionary.
        Example: 
        { 
            'u_id' : 0,
            'email' : example_email,
            'name_first' : Firs,
            'name_last' : Last,
            'hash' : encrypted password,
            'token' : token,
            'premission : 1,
            'handle_str' :firstlast             

        }
        If token is not found in the datastore registered to any user
        it returns False """

    for user in registered_users_store['registered_users']:
        if user['token'] == token:
            return user
    return False
    
def reset_message():
    """This function reset the message and returns nothing"""
    global message_list
    message_list[:] = [
        # {

        # }
    ]

def get_message():
    """This function get the list of dictionary of messages and returns it"""
    global message_list
    return message_list

def get_profile(u_id):
    '''Gets a user profile via u_id instead of token. Used in the user_profile function'''
    for user in registered_users_store['registered_users']:
        if user['u_id'] == u_id:
            formatted_user = {
                "u_id" : user['u_id'],
                "email" : user['email'],    
                "name_first" : user['name_first'],  
                "name_last" : user['name_last'],
                "handle_str" : user['handle_str']
            }
            return formatted_user
    raise InputError

def set_name(token, name_first, name_last):
    '''Changes the first and last name of a user'''
    user = search_database(token)
    user['name_first'] = name_first
    user['name_last'] = name_last

def set_email(token, email):
    '''Changes the email of a user'''
    user = search_database(token)
    user['email'] = email

def set_handle(token, handle_str):
    '''Changes the handle of a user'''
    user = search_database(token)
    user['handle_str'] = handle_str

def check_email_already_used(email):
    '''Checks if an email is already being used'''
    for user in registered_users_store['registered_users']:
        if user['email'] == email:
            return True
    return False

def check_handle_str_already_used(handle_str):
    '''Checks if a handle is already being used'''
    for user in registered_users_store['registered_users']:
        if user['handle_str'] == handle_str:
            return True
    return False
    
def turn_on_standup(channel_id, length):
    '''makes a channel into standup mode if it's not already. The standup_finish_time is equal to
    the present time plus the length'''
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            if not channel['is_in_standup']:
                channel['is_in_standup'] = True
                current_dt = datetime.now()
                timestamp = current_dt.replace(tzinfo=timezone.utc).timestamp()
                channel['standup_finish_time'] = timestamp + length
                return
            if channel['is_in_standup']:
                raise InputError(description='An active standup is currently running in this channel')
    raise InputError(description='Not a valid channel ID')

def turn_off_standup(channel_id):
    '''deactivates stand up mode for a channel and sends the messages in standup queue'''
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            channel['is_in_standup'] = False
            channel['standup_finish_time'] = None
            return




def check_channel_exists(channel_id):
    '''check if a channel with channel_id exists'''
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            return True
    return False

def check_user_in_channel(token, channel_id):
    '''check if a user (identified by their token) is a member of a channel (identified by channel id)'''
    person = get_u_id(token)
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            for mem_id in channel['all_members']:
                if mem_id == person:
                    return True
    return False

def check_standup_happening(channel_id):
    '''check if a standup is happening in a channel'''
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            if channel['is_in_standup']:
                return True
    return False

def get_standup_finish_time(channel_id):
    '''get the finishing time for a standup'''
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            return channel.get('standup_finish_time')

def get_standup_queue():
    global standup_queue
    return standup_queue


def get_profile_allinfo(u_id):
    '''Gets a user profile via u_id instead of token. Used in the user_profile function'''
    for user in registered_users_store['registered_users']:
        if user['u_id'] == u_id:
            return user
    raise InputError

def get_list_of_channels():
    global list_of_channels
    return list_of_channels
    
