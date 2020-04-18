from error import AccessError, InputError
from auth import auth_register
from user import user_profile
from channels import channels_list, channels_listall, channels_create
from channel import channel_addowner, channel_removeowner, channel_invite, channel_details, channel_join, channel_leave, channel_messages
from message import message_send, message_remove
from helper_functions import register_valid_user, register_another_valid_user
from database import restore_channel_database, restore_database, reset_message
import pytest


"""

Channel Tests 2
Written by Aaron Lin
--------------------
Implemtation tests for channel_invite, channel_details, channel_messages

"""

"""    ERROR TESTS FOR CHANNEL_INVITE_USER    """
    
### Test when inviting user to a channel with invalid channel_id - gives InputError (where u_id is valid)
def test_invite_invalid_channel_id():
    restore_database()
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel_id + 1, user['u_id'])
    #   testing same issue with a separate but invalid channel_id
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel_id + 10, user['u_id'])

### Test when inviting an INVALID u_id - gives InputError
def test_invite_invalid_u_id():
    restore_database()
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel_id, user['u_id'] + 1)
    #   testing same issue with a separate but invalid u_id
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel_id, user['u_id'] + 10)
        
### test when a non-member of channel invites another user - AccessError
def test_invite_authorised_user_invalid():
    restore_database()
    restore_channel_database()
    #   Create user and channel
    user_in_channel = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel_id = channels_create(user_in_channel['token'], 'valid_channel', True)['channel_id']
    
    #   Register the two users not in channel
    user_not_in_channel = register_valid_user()
    another_user_not_in_channel = register_another_valid_user()
    
    #   AccessError When user_not_in_channel invites another_user_not_in_channel
    with pytest.raises(AccessError) as e:
         channel_invite(user_not_in_channel['token'], channel_id, another_user_not_in_channel['u_id'])
    
### Test if function gives AccessError when invalid token passed
def test_invite_invalid_token():
    restore_database()
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   Raise AccessError
    with pytest.raises(AccessError) as e:
        channel_invite('hopefullythisisnotavalidtoken', channel_id, user['u_id'])
        
        
"""    TEST FOR NORMAL FUNCTIONING OF INVITE_USER    """
    
### Test for normal activity of channel_invite function
def test_channel_invite_normal():
    restore_database()
    restore_channel_database()
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   make sure user is part of channel
    user_channels = channels_list(user['token'])['channels']
    assert user_channels[0]['channel_id'] == channel_id
    
    #   check whether user can now invite user2 to the channel
    user2 = register_another_valid_user()
    channel_invite(user['token'], channel_id, user2['u_id'])
    #   check if user is a member of the channel
    user2_channels = channels_list(user2['token'])['channels']
    assert user2_channels[0]['channel_id'] == channel_id


"""    ERROR TESTS FOR CHANNEL_DETAILS    """
    
### Test when authorised user is not part of the channel - AccessError
def test_details_not_in_channel():
    restore_database()
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   create two users not in channel
    user_not_in_channel = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    user_also_not_in_channel = auth_register('name3@mail.com', 'password1', 'Tim', 'He')
    
    #   raises AccessError
    with pytest.raises(AccessError) as e:
        channel_details(user_not_in_channel['token'], channel_id)
    with pytest.raises(AccessError) as e:
        channel_details(user_also_not_in_channel['token'], channel_id)
        
### Test when checking channel with invalid_channel_id - InputError
def test_details_invalid_channel_id():
    restore_database()
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']

    #   raise InputError
    with pytest.raises(InputError) as e:
        channel_details(user['token'], channel_id + 1)
    with pytest.raises(InputError) as e:
        channel_details(user['token'], channel_id + 10)

### Test if function gives AccessError when invalid token passed
def test_details_invalid_token():
    restore_database()
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   Raise AccessError
    with pytest.raises(AccessError) as e:
        channel_details('hopefullythisisnotavalidtoken', channel_id)


"""    TESTS FOR NORMAL FUNCTION OF CHANNEL_DETAILS    """
        
### test for normal function of channel_details ###
def test_channel_details_normal():
    restore_database()
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
#   test for channel with only one member
    #   run channel_details
    details = channel_details(user['token'], channel_id)
    #   make sure channel details is the same as actual details
    assert details['name'] == 'valid_channel'
    owner = [{'u_id': user['u_id'], 'name_first': 'First', 'name_last': 'Last'}]
    assert details['owner_members'] == owner
    #   same as 'owner_members' as the only member is the owner
    assert details['all_members'] == owner
    
#   test for channel with only one member
    #   Invite user2 to the channel
    user2 = register_another_valid_user()
    channel_invite(user['token'], channel_id, user2['u_id'])
    
    #   run channel_details on two members
    details = channel_details(user['token'], channel_id)
    
    #   make sure channel details is the same as actual details
    assert details['name'] == 'valid_channel'
    #   assuming the first person added becomes the owner
    owner = {'u_id': user['u_id'], 'name_first': 'First', 'name_last': 'Last'}
    owner_list = [owner]
    assert details['owner_members'] == owner_list
    #   now we have two members but only one owner
    member1 = {'u_id': user2['u_id'], 'name_first': 'Anotherfirst', 'name_last': 'Anotherlast'}
    member_list = [owner, member1]
    assert details['all_members'] == member_list


"""    TEST FOR ERRORS IN CHANNEL_MESSAGES    """
    
"""### Test when checking channel with no messages - AccessError
def test_no_messages():
    reset_message()
    restore_database()
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   Raise AccessError
    with pytest.raises(AccessError) as e:
        channel_messages(user['token'], channel_id, 0)
"""
### Test when checking channel with INVALID CHANNEL_ID - InputError
def test_messages_invalid_chanel_id():
    reset_message()
    restore_database()
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   send a message - prevents AccessError
    message_send(user['token'], channel_id, "abcde")
    
    #   raise InputError for different cases
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel_id + 1, 0)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel_id + 10, 0)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel_id -10, 0)
    
### Test for when 'start' is greater than total messages - InputError
def test_message_out_of_range():
    reset_message()
    restore_database()
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   send 10 messages to channel
    for i in range(10):
        message_send(user['token'], channel_id, "abcde")
        
    total_messages = 10
    
    #   raise InputError
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel_id, total_messages + 1)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel_id, total_messages + 10)
    
### Test when authorised user is not part of the channel - AccessError
def test_messages_not_in_channel():
    reset_message()
    restore_database()
    restore_channel_database()
    #   create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   create users who are not in the channel
    user_not_in_channel = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    user_also_not_in_channel = auth_register('name3@mail.com', 'password1', 'Tim', 'He')
    
    #   send 10 messages to channel
    for i in range(10):
        message_send(user['token'], channel_id, "abcde")
        
    total_messages = 10
    
    with pytest.raises(AccessError) as e:
        channel_messages(user_not_in_channel['token'], channel_id, total_messages - 1)
    with pytest.raises(AccessError) as e:
        channel_messages(user_also_not_in_channel['token'], channel_id, total_messages - 1)
        
### Test if function gives AccessError when invalid token passed
def test_messages_invalid_token():
    reset_message()
    restore_database()
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    #   send a message
    message_send(user['token'], channel_id, "abcde")
    
    #   Raise AccessError
    with pytest.raises(AccessError) as e:
        channel_messages('hopefullythisisnotavalidtoken', channel_id, 0)


"""    TEST NORMAL FUNCTIONING OF CHANNEL_MESSAGES    """
            
### Test the normal functioning of channel_messages ###     
def test_channel_messages_normal():
    reset_message()
    restore_database()
    restore_channel_database()
    #   Create user and channel
    user = register_valid_user()
    channel_id = channels_create(user['token'], 'valid_channel', True)['channel_id']
    
    first_id = message_send(user['token'], channel_id, 'abcde-1')
    
    print("First Message")
    #   check if channel_messages are correct in these channel as well as 'start' and 'end' points
    message = channel_messages(user['token'], channel_id, 0)
    assert message['messages'][0]['message'] == f'abcde-1'
    assert message['start'] == 0
    assert message['end'] == -1
    
    message_send(user['token'], channel_id, 'abcde0')
    message_send(user['token'], channel_id, 'abcde1')
    message_remove(user['token'], first_id)
    print("Message0")
    #   check if channel_messages are correct in these channel as well as 'start' and 'end' points
    message0 = channel_messages(user['token'], channel_id, 0)
    assert message0['messages'][0]['message'] == f'abcde0'
    assert message0['messages'][1]['message'] == f'abcde1'
    assert message0['start'] == 0
    assert message0['end'] == -1
    
    #   send 124 messages into channel
    for i in range(2,124):
        message_send(user['token'], channel_id, f'abcde{i}')
    print("Message1")
    #   check if channel_messages are correct in these channel as well as 'start' and 'end' points
    message1 = channel_messages(user['token'], channel_id, 0)
    for i in range(50):
        print(f"message{i} = {message1['messages'][i]['message']}")
        assert message1['messages'][i]['message'] == f'abcde{i}'
    assert message1['start'] == 0
    assert message1['end'] == 50
    
    print("Message2")
    message2 = channel_messages(user['token'], channel_id, 50)
    for i in range(50):
        assert message2['messages'][i]['message'] == f'abcde{i+50}'
    assert message2['start'] == 50
    assert message2['end'] == 100

