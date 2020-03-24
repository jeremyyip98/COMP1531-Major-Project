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
