from error import AccessError, InputError
from auth import auth_register
from user import user_profile
from channels import channels_list, channels_listall, channels_create
from channel import channel_addowner, channel_removeowner, channel_invite, channel_details, channel_join, channel_leave, channel_messages
from message import message_send
from helper_functions import register_valid_user, register_another_valid_user
import pytest

    """    ERROR TESTS FOR CHANNEL_INVITE_USER    """
    
### Test when inviting user to a channel with invalid channel_id - gives InputError (where u_id is valid)
def test_invite_invalid_channel_id():
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'] + 1, user['u_id'])
    #   testing same issue with a separate but invalid channel_id
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'] + 10, user['u_id'])

### Test when inviting an INVALID u_id - gives InputError
def test_invite_invalid_u_id():
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user['u_id'] + 1)
    #   testing same issue with a separate but invalid u_id
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user['u_id'] + 10)
        
### test when a non-member of channel invites another user - AccessError
def test_invite_authorised_user_invalid():
    restore_channel_database()
    #   Create user and channel
    user_in_channel = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel = create_valid_channel(user_in_channel['token'] + 'invalid', 'valid_channel')
    
    #   Register the two users not in channel
    user_not_in_channel = register_valid_user()
    another_user_not_in_channel = register_another_valid_user()
    
    #   AccessError When user_not_in_channel invites another_user_not_in_channel
    with pytest.raises(AccessError) as e:
         channel_invite(user_not_in_channel['token'], channel['channel_id'], another_user_not_in_channel['u_id'])
         
### Test when member of channel invites themselves - InputError 
def test_invite_self():
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   Raise InputError
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user['u_id'])
    
### Test if function gives AccessError when invalid token passed
def test_invite_invalid_token():
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   Raise AccessError
    with pytest.raises(AccessError) as e:
        channel_invite('hopefullythisisnotavalidtoken', channel['channel_id'], user['u_id'])
        
        
    """    TEST FOR NORMAL FUNCTIONING OF INVITE_USER    """
    
### Test for normal activity of channel_invite function
def test_channel_invite_normal():
    restore_channel_database()
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   make sure user is part of channel
    user_channels = channels_list(user['token'])
    assert user_channels['channels'][0]['channel_id'] == channel['channel_id']
    
    #   check whether user can now invite user2 to the channel
    user2 = register_another_valid_user()
    channel_invite(user['token'], channel['channel_id'], user2['u_id'])
    #   check if user is a member of the channel
    user2_channels = channels_list(user2['token'])
    assert user2_channels['channels'][0]['channel_id'] == channel['channel_id']


    """    ERROR TESTS FOR CHANNEL_DETAILS    """
    
### Test when authorised user is not part of the channel - AccessError
def test_details_not_in_channel():
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   create two users not in channel
    user_not_in_channel = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    user_also_not_in_channel = auth_register('name3@mail.com', 'password1', 'Tim', 'He')
    
    #   raises AccessError
    with pytest.raises(AccessError) as e:
        channel_details(user_not_in_channel['token'], channel['channel_id'])
    with pytest.raises(AccessError) as e:
        channel_details(user_also_not_in_channel['token'], channel['channel_id'])
        
### Test when checking channel with invalid_channel_id - InputError
def test_details_invalid_channel_id():
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')

    #   raise InputError
    with pytest.raises(InputError) as e:
        channel_details(user['token'], channel['channel_id'] + 1)
    with pytest.raises(InputError) as e:
        channel_details(user['token'], channel['channel_id'] + 10)

### Test if function gives AccessError when invalid token passed
def test_details_invalid_token():
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   Raise AccessError
    with pytest.raises(AccessError) as e:
        channel_details('hopefullythisisnotavalidtoken', channel['channel_id'])


    """    TESTS FOR NORMAL FUNCTION OF CHANNEL_DETAILS    """
        
### test for normal function of channel_details ###
def test_channel_details_normal():
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
#   test for channel with only one member
    #   run channel_details
    details = channel_details(user['token'], channel['channel_id'])
    #   make sure channel details is the same as actual details
    assert details['name'] == 'valid_channel'
    owner = {'u_id': user['u_id'], 'name_first': 'John', 'name_last': 'Doe'}
    assert details['owner_members'] == owner
    #   same as 'owner_members' as the only member is the owner
    assert details['all_members'] == owner
    
#   test for channel with only one member
    #   Invite user2 to the channel
    user2 = register_another_valid_user()
    channel_invite(user['token'], channel['channel_id'], user2['u_id'])
    
    #   run channel_details on two members
    details = channel_details(user['token'], channel['channel_id'])
    
    #   make sure channel details is the same as actual details
    assert details['name'] == 'valid_channel'
    #   assuming the first person added becomes the owner
    owner = {'u_id': user['u_id'], 'name_first': 'John', 'name_last': 'Doe'}
    assert details['owner_members'] == owner
    #   now we have two members but only one owner
    member1 = {'u_id': user2['u_id'], 'name_first': 'Ben', 'name_last': 'Ny'}
    member_list = [owner, member1]
    assert details['all_members'] == member_list


    """    TEST FOR ERRORS IN CHANNEL_MESSAGES    """
    
### Test when checking channel with no messages - AccessError
def test_no_messages():
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   Raise AccessError
    with pytest.raises(AccessError) as e:
        channel_messages(user['token'], channel['channel_id'], 0)

### Test when checking channel with INVALID CHANNEL_ID - InputError
def test_messages_invalid_chanel_id():
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   send a message - prevents AccessError
    message_send(user['token'], channel['channel_id'], "abcde")
    
    #   raise InputError for different cases
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'] + 1, 0)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'] + 10, 0)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'] -10, 0)
    
### Test for when 'start' is greater than total messages - InputError
def test_message_out_of_range():
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   send 10 messages to channel
    for i in range(10):
        message_send(user['token'], channel['channel_id'], "abcde")
        
    total_messages = 10
    
    #   raise InputError
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'], total_messages + 1)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'], total_messages + 10)
    
### Test when authorised user is not part of the channel - AccessError
def test_messages_not_in_channel():
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   create users who are not in the channel
    user_not_in_channel = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    user_also_not_in_channel = auth_register('name3@mail.com', 'password1', 'Tim', 'He')
    
    with pytest.raises(AccessError) as e:
        channel_messages(user_not_in_channel['token'], channel['channel_id'], total_messages - 1)
    with pytest.raises(AccessError) as e:
        channel_messages(user_also_not_in_channel['token'], channel['channel_id'], total_messages - 1)
        
### Test if function gives AccessError when invalid token passed
def test_messages_invalid_token():
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   send a message
    message_send(user['token'], channel['channel_id'], "abcde")
    
    #   Raise AccessError
    with pytest.raises(AccessError) as e:
        channel_messages('hopefullythisisnotavalidtoken', channel['channel_id'], 0)


    """    TEST NORMAL FUNCTIONING OF CHANNEL_MESSAGES    """
            
### Test the normal functioning of channel_messages ###     
def test_channel_messages_normal():
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel = create_valid_channel(user['token'], 'valid_channel')
    
    #   send 124 messages into channel
    for i in range(124):
        message_send(user['token'], channel['channel_id'], f'abcde{i}')
    
    #   check if channel_messages are correct in these channel as well as 'start' and 'end' points
    message0 = channel_messages(user['token'], channel['channel_id'], 0)
    for i in range(50):
        assert message0['messages'][i]['message'] == f'abcde{i}'
    assert message0['start'] == 0
    assert message0['end'] == 50
        
    message1 = channel_messages(user['token'], channel['channel_id'], 50)
    for i in range(50, 100):
        assert message1['messages'][i]['message'] == f'abcde{i}'
    assert message0['start'] == 50
    assert message0['end'] == 100
    
    #   check when function reaches end of messages
    message2 = channel_messages(user['token'], channel['channel_id'], 100)
    for i in range(100, 124):
        assert message1['messages'][i]['message'] == f'abcde{i}'
    assert message0['start'] == 100
    assert message0['end'] == -1

