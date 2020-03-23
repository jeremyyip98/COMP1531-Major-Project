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

message_list = [{
    # channel_id (int) (extra element that is not mentioned in spec)
    # message_id (int)
    # u_id (int)
    # message (string)
    # time_created (integer (unix timestamp))
    # reacts (list of dictionaries)
    # is_pinned (Boolean?)
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
