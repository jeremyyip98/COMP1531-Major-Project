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
                                  # 'u_id' : u_id,
                                  # 'email' : email,
                                  # 'name_first' : name_first,
                                  # 'name_last' : name_last,
                                  # 'hash' : hash,
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
    if search_database(token):
        return True
    else:
        raise AccessError

def get_u_id(token):
    return search_database(token)['u_id']

def get_email(token):
    return search_database(token)['email']

def search_database(token):
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