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
    list_of_channels.append(new_channel)
    return re_channel_id