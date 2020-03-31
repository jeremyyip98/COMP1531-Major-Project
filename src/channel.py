"""
UNSW COMP1531 Iteration 2
channel.py
Written by Jackie Cai z5259449
"""
from database import channel_ids, list_of_channels, search_database, get_u_id, get_profile, get_channel, get_message, get_formatted_user
from error import AccessError, InputError

def channel_join(token, channel_id):
    """gets a token from the user and channel_id that the peron can join
    and adds them to the channel (checks if channel is public to allow join)"""
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    user_id = get_u_id(token)
    user = search_database(token)
    #iterate though the channels
    for chan in list_of_channels['channels']:
        if chan['channel_id'] == channel_id:
            #if the user is already in the channel raises input error
            for usr in chan['all_members']:
                if usr == user_id:
                    raise InputError(description="Already in Channel")
            #checks if it's public and user is owner
            if not chan['is_public'] and user['permission_id'] == 2:
                raise AccessError(description='Not an owner and Private Channel')
            else:
                chan['all_members'].append(user_id)
                return
    raise InputError(description="Channel ID is not a valid channel")
def channel_leave(token, channel_id):
    """a user leaves the channel including owner"""
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    user_id = get_u_id(token)
    #iterate through channel
    for chan in list_of_channels['channels']:
        #found a channel with the id
        if chan['channel_id'] == channel_id:
            for usr in chan['all_members']:
                #found the user in the channel
                if usr == user_id:
                    chan['all_members'].remove(user_id)
                    #check if the user was an owner
                    for own in chan['owner_members']:
                        #if so removes from owner as well
                        if own == user_id:
                            chan['owner_members'].remove(user_id)
                    return
            raise AccessError(description='Not a member of the Channel')
    raise InputError(description="Channel ID is not a valid channel")
def channel_addowner(token, channel_id, u_id):
    """Another owner adds a member as owner"""
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    user = get_formatted_user(token)
    for chan in list_of_channels['channels']:
        #found channel
        if chan['channel_id'] == channel_id:
            #checking if the user given is already a owner or if the user adding is not an owner
            if u_id in chan['owner_members']:
                raise InputError(description='Already an Owner of the channel')
            #checks if the token person is a owner of slackr
            if user['permission_id'] == 1:
                chan['owner_members'].append(u_id)
                return
            if user['u_id'] not in chan['owner_members']:
                raise AccessError(description='User is not an Owner of Slackr or Channel')
            else:
                chan['owner_members'].append(u_id)
                return
    raise InputError(description='Channel ID is not a valid channel')
def channel_removeowner(token, channel_id, u_id):
    """Another owner removes and owner from the channel but the member is stil in the channel"""
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    #set user as is_valid returns user info if token is valid
    user = is_valid
    for chan in list_of_channels['channels']:
        if chan['channel_id'] == channel_id:
            if u_id not in chan['owner_members']:
                raise InputError(description='No Owner found in Channel')
            if user['permission_id'] == 1:
                chan['owner_members'].remove(u_id)
                return
            if user['u_id'] not in chan['owner_members']:
                raise AccessError(description='User is not an Owner of Slackr or Channel')
            else:
                chan['owner_members'].remove(u_id)
                return
    raise InputError(description='Channel ID is not a valid channel')

"""
UNSW COMP1531 Iteration 2
channel.py
Written by Aaron Lin z5258280
"""

# Invites user with u_id to join channel with channel_id
# Added immediately once invited
def channel_invite(token, channel_id, u_id):
    # check if the token is valid
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
        
    # authorised user is user who is in the channel and invites another user
    authorised_user = get_formatted_user(token)
    # invited_user is user who is invited and added to the channel
    # inputError raised in get_profile() when u_id not a valid user
    invited_user = get_profile(u_id)
    
    found_authorised_user = False
    found_channel = False
    for channel in list_of_channels['channels']:
        # found the right channel and add user to channel
        if channel['channel_id'] == channel_id:
            found_channel = True
            # searching through members in the channel
            for members in channel['all_members']:
                # checking if authorised user in the channel
                if authorised_user['u_id'] == members:
                    found_authorised_user = True
                    channel['all_members'].append(invited_user['u_id'])
    
    # no channel with channel_id
    if found_channel is False:
        raise InputError(description='Channel_ID does not refer to valid channel')
        
    # raise accessError if authorised user is not in channel
    if found_authorised_user is False:
        raise AccessError(description='Authorised user not in channel')
    
def channel_details(token, channel_id):
    """Gives details of channel"""
    # check if the token is valid
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    
    # authorised user is user who is in the channel and invites another user
    authorised_user = get_formatted_user(token)
    found_channel = False
    found_authorised_user = False
    
    details = {}
    
    for channel in list_of_channels['channels']:
        # found the right channel
        if channel['channel_id'] == channel_id:
            # found the channel
            found_channel = True
            
            # check if authorised user is in the channel
            for members in channel['all_members']:
                if members == authorised_user['u_id']:
                    # authorised user is in the channel
                    found_authorised_user = True

            # setting details to have the details of this channel
            details['name'] = channel['channel_name']
            
            # creating a list of dicts for 'owner_members' and 'all_members'
            owner_list = []
            member_list = []
            
            # adding into owner_list
            for owner_id in channel['owner_members']:
                owner_details = get_profile(owner_id)
                owner_list.append({ 'u_id': owner_id, 
                                    'name_first': owner_details['name_first'],
                                    'name_last': owner_details['name_last']
                                 })
            
            # adding into member_list
            for member_id in channel['all_members']:
                member_details = get_profile(member_id)
                member_list.append({ 'u_id': member_id, 
                                    'name_first': member_details['name_first'],
                                    'name_last': member_details['name_last']
                                  })
            
            details['owner_members'] = owner_list
            details['all_members'] = member_list
        
    if found_channel is False:
        raise InputError(description='Channel_ID is not a valid channel')
        
    if found_authorised_user is False:
        raise AccessError(description='Authorised user is not a member of channel with channel_id')
        
    return details
    
def channel_messages(token, channel_id, start):
    # check if the token is valid
    is_valid = search_database(token)
    if is_valid is False:
        raise AccessError(description='Invalid Token')
    
    # authorised user is user who is in the channel and invites another user
    authorised_user = is_valid
    found_channel = False
    found_authorised_user = False
    num_total_messages = 0
    message_ids = []
    end = start
    
    # get_channel to get the message_list inside the channel
    for chan in get_channel():
        if chan['channel_id'] == channel_id:
            end_of_list = chan['channel_messages'][-1]
            num_total_messages = len(chan['channel_messages'])
            # add from message_list to messages
            for msg_id in chan['channel_messages']:
                if (end - start > 50):
                    break
                elif (end - start <= 50 and msg_id == end_of_list):
                    end = -1
                else:
                    id_in_list = False
                    for ids in message_ids:
                        if msg_id == ids:
                            id_in_list = True
                    if id_in_list is False:
                        message_ids.append(msg_id)
                        end += 1
                # incrementing total_message
                #num_total_messages += 1
    end -= 1
    
    print(f"start = {start}, end = {end}, num_total_messages = {num_total_messages}")
    
    if start >= num_total_messages:
        raise InputError('Start is greater than or equal to total messages in the channel')
                    
    # initialise empty messages list
    messages = []
    
    message_list = get_message()   
    for ids in message_ids:      
        for msg_dict in message_list:
            if msg_dict['message_id'] == ids:
                # adds the message dict to messages list
                messages.append(msg_dict)
    
    for channel in list_of_channels['channels']:
        # found the right channel
        if channel['channel_id'] == channel_id:
            # found the channel
            found_channel = True
            
            # check if authorised user is in the channel
            for members in channel['all_members']:
                if members == authorised_user['u_id']:
                    # authorised user is in the channel
                    found_authorised_user = True
            
    if found_channel is False:
        raise InputError(description='Channel_ID is not a valid channel')
        
    if found_authorised_user is False:
        raise AccessError(description='Authorised user is not a member of channel with channel_id')    
    
    return {'messages': messages, 'start': start, 'end': end}
