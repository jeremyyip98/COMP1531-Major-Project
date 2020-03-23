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