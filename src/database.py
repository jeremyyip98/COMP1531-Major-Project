message_list = [{
    # channel_id (int) (extra element that is not mentioned in spec)
    # message_id (int)
    # u_id (int)
    # message (string)
    # time_created (integer (unix timestamp))
    # reacts (list of dictionaries)
    # is_pinned (Boolean?)
}]

react_list = [{
    # react_id (int)
    # u_ids (list)
    # is_this_user_reacted (boolean?)
}]

def reset_message():
    """This function reset the message and returns nothing"""
    global message_list
    message_list = [{
 
    }]

def get_message():
    """This function get the list of dictionary of messages and returns it"""
    global message_list
    return message_list

def reset_react():
    """This function reset the react and returns nothing"""
    global react_list
    react_list = [{
 
    }]

def get_react():
    """This function get the list of dictionary of react and returns it"""
    global react_list
    return react_list


