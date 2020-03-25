from error import AccessError

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
                                  #  }    
                                ]

                        }

channel_ids = [0]

list_of_channels = {
                            'channels' :
                            [
                              #{
                              #'channel_id' : channel_id,
                              #'channel_name' : channel_name
                              #'is_public' : boolean
                              #'owner_members' : [owners]
                              #'all_members : [all_members]
                              # }
                            ]
}
def restore_channel_databse():
    """reseting the channel database to clear it"""
    global list_of_channels
    list_of_channels.clear()
    list_of_channels = {
        'channels' :
        [
            #{
            # }
        ]
}
message_list = [{
    # message_id (int)
    # u_id (int)
    # message (string)
    # time_created (integer (unix timestamp))
    # reacts (list of dictionaries)
    # is_pinned (Boolean)
}]

# Extra datatype that is not mentioned in the spec
channel_list = [{
    # channel_id (int)
    # channel_messages (list of message_id (int))
}]

def check_token(token):
    """ Takes token raises Access Error if the token is not linked to any user,
        otherwise it returns True """
    if search_database(token):
        return True
    else:
        raise AccessError

def get_u_id(token):
    """ Takes token and returns the u_id of user token belongs to"""
    return search_database(token)['u_id']

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
    message_list = [{

    }]

def get_message():
    """This function get the list of dictionary of messages and returns it"""
    global message_list
    return message_list

def get_channel():
    """This function create a relationship between channel and message,
    and returns a list of dictionaries that contain it"""
    global channel_list
    return channel_list