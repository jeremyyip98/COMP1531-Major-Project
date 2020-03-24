from error import AccessError, InputError
from auth import auth_register
from user import user_profile
from channels import channels_list, channels_listall, channels_create
from channel import channel_addowner, channel_removeowner, channel_invite, channel_details, channel_join, channel_leave, channel_messages
from message import message_send
import pytest

### Tests the channel_invite() function for errors ###
def test_channel_invite_errors():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    
#   test when inviting user to a channel with invalid channel_id - gives InputError (where u_id is valid)
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'] + 1, user['u_id'])
    #   testing same issue with a separate but invalid channel_id
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'] + 10, user['u_id'])
        
#   test when inviting an INVALID u_id - gives InputError
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user['u_id'] + 1)
    #   testing same issue with a separate but invalid u_id
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user['u_id'] + 10)

#   test when a non-member of channel invites another user - AccessError
    user2 = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    user3 = auth_register('name3@mail.com', 'password1', 'Tim', 'He')
    with pytest.raises(AccessError) as e:
         channel_invite(user2['token'], channel['channel_id'], user3['u_id'])
    
#   test when a member of channel invites themselves - InputError
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user['u_id'])
        
# test if function gives AccessError when invalid token passed
    with pytest.raises(AccessError) as e:
        channel_invite('hopefullythisisnotavalidtoken', channel['channel_id'], user['u_id'])
         
### Test for normal activity of channel_invite function ###
def test_channel_invite_normal():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    
    #   make sure user is part of channel
    user_channels = channels_list(user['token'])
    assert user_channels['channels'][0]['channel_id'] == channel['channel_id']
    
    #   check whether user can now invite user2 to the channel
    user2 = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    channel_invite(user['token'], channel['channel_id'], user2['u_id'])
    #   check if user is a member of the channel
    user2_channels = channels_list(user2['token'])
    assert user2_channels['channels'][0]['channel_id'] == channel['channel_id']


### test error cases in channel_details function ###
def test_channel_details_errors():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    
#   test when authorised user is not part of the channel - AccessError
    user2 = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    user3 = auth_register('name3@mail.com', 'password1', 'Tim', 'He')
    with pytest.raises(AccessError) as e:
        channel_details(user2['token'], channel['channel_id'])
    with pytest.raises(AccessError) as e:
        channel_details(user3['token'], channel['channel_id'])
      
#   test when checking channel with invalid_channel_id - InputError
    with pytest.raises(InputError) as e:
        channel_details(user['token'], channel['channel_id'] + 1)
    with pytest.raises(InputError) as e:
        channel_details(user['token'], channel['channel_id'] + 10)
        
# test if function gives AccessError when invalid token passed
    with pytest.raises(AccessError) as e:
        channel_invite('hopefullythisisnotavalidtoken', channel['channel_id'])
        
        
### test for normal function of channel_details ###
def test_channel_details_normal():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    
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

    user2 = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
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

### Testing the errors in channel_messages ###
def test_channel_messages_errors():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    #   creates channel and assumes user is now owner
    channel = channels_create(user['token'], 'valid_channel', True)
    
    #   test when there is no messages - assume AccessError
    with pytest.raises(AccessError) as e:
        channel_messages(user['token'], channel['channel_id'], 0)
        
    #   send a message
    message_send(user['token'], channel['channel_id'], "abcde")
    
    #   test when checking channel with INVALID CHANNEL_ID - InputError
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'] + 1, 0)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'] + 10, 0)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'] -10, 0)
        
    #   send 9 messages to channel
    for i in range(1, 10):
        message_send(user['token'], channel['channel_id'], "abcde")
        
    #   check if start is greater than total messages
    total_messages = 10 # 9 messages + first one
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'], total_messages + 1)
    with pytest.raises(InputError) as e:
        channel_messages(user['token'], channel['channel_id'], total_messages + 10)
    
    #   test when authorised user is not part of the channel - AccessError
    user2 = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    user3 = auth_register('name3@mail.com', 'password1', 'Tim', 'He')
    with pytest.raises(AccessError) as e:
        channel_messages(user2['token'], channel['channel_id'], total_messages-1)
    with pytest.raises(AccessError) as e:
        channel_messages(user3['token'], channel['channel_id'], total_messages-1)
        
    # test if function gives AccessError when invalid token passed
    with pytest.raises(AccessError) as e:
        channel_invite('hopefullythisisnotavalidtoken', channel['channel_id'], 0)
        
### Test the normal functioning of channel_messages ###     
def test_channel_messages_normal():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    #   creates channel and assumes user is now owner
    channel = channels_create(user['token'], 'valid_channel', True)
    
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
