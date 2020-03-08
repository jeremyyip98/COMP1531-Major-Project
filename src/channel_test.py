from error import AccessError, InputError
from auth import auth_register
from user import user_profile
from channels import channels_list, channels_listall, channels_create
from channel import channel_addowner, channel_removeowner, channel_invite, channel_details, channel_join, channel_leave, channel_messages
from message import message_send
import pytest


def test_channels_create():
    #test invalid token
    with pytest.raises(AccessError) as e:
        channels_create('hopefullythisnotavalidtoken', 'a', True)
    #test if there is an input error when character string is greater than 20
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    with pytest.raises(InputError) as e:
        channels_create(user1['token'], 'a' * 21, True)
    #test if it returns the right ID
    channel1 = channels_create(user1['token'], 'My Channel', True)
    channelList = channels_listall(user1['token'])
    assert channel1['channel_id'] == channelList['channels'][0]['channel_id']

def test_channel_list():
    #should only show the channels the user given is in 
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name2@mail.com', 'password1', 'Tim', 'Lift')
    
    channel1 = channels_create(user1['token'], 'My Channel', True)
    channel2 = channels_create(user2['token'], 'Second Channel', False)
    #test invalid token
    with pytest.raises(AccessError) as e:
        channels_list('hopefullythisnotavalidtoken')
    #create chanel_list
    channelList = channels_list(user1['token'])
    #make sure there is only one channel
    assert channelList['channels'][0]['channel_id'] == channel1['channel_id']
    assert len(channelList['channels']) == 1
    
    #check info is right
    details = channel_details(user1['token'], channel1['channel_id'])
    assert details['name'] == channelList['channels'][0]['name']
    
    #make second channellist to test if it only shows for user2
    channelList2 = channels_list(user2['token'])
    
    assert channelList2['channels'][0]['channel_id'] == channel2['channel_id']
    assert len(channelList2['channels']) == 1
    #make sure all the details are right
    details = channel_details(user2['token'], channel2['channel_id'])
    assert details['name'] == channelList2['channels'][0]['name']
    
def test_channel_listall():
    #check if inputed invalid token
    with pytest.raises(AccessError) as e:
        channels_listall('hopefullythisnotavalidtoken')
    #when called the channel list all should list all channels including id 
    #and name regardless
    #if the user is in the channel or not (assuming thats what specs says)
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name2@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    channel2 = channels_create(user2['token'],'Second Channel', False)
    channelList = channels_listall(user1['token'])
    #make sure it shows both channels for one user even if user is not in
    #the channel
    assert channelList['channels'][0]['channel_id'] == channel1['channel_id']
    assert channelList['channels'][1]['channel_id'] == channel2['channel_id']
    


def test_channel_addowner():
    #assume user1 is owner of channel when he makes the channel
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name2@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    
    #check that when inputed wrong token gives access error
    with pytest.raises(AccessError) as e:
        channel_addowner('hopefullythisnotavalidtoken', channel1['channel_id'], user1['u_id'])

    #test if the channel adds user1 again it gives InputError
    with pytest.raises(InputError) as e:
        channel_addowner(user1['token'], channel1['channel_id'], user1['u_id'])
    
    #test if the channel tries to add channel_id invalid id
    with pytest.raises(InputError) as e:
        channel_addowner(user1['token'], channel1['channel_id'], user1['u_id'])
    
    #invites user2 to channel
    channel_invite(user1['token'],channel1['channel_id'], user2['u_id'])

    #test if the unauthorises user tries to add himself as owner
    with pytest.raises(AccessError) as e:
        channel_addowner(user2['token'], channel1['channel_id'], user2['u_id'])
    
    #adds user2 as owner
    channel_addowner(user1['token'], channel1['channel_id'], user2['u_id'])

    details = channel_details(user2['u_id'], channel1['channel_id'])
    #assert that user 2 is in owners through the details function
    user2_profile = user_profile(user2['token'], user2['u_id'])
    assert details['owner_members'][1]['name_first'] == user2_profile['user']['name_first']
    

def test_channel_remove_owner():
    #assume user1 is owner of channel when he makes the channel
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name2@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    details = channel_details(user1['u_id'], channel1['channel_id'])
    
    #Test that when inputed invalid token access error is raised
    with pytest.raises(AccessError) as e:
        channel_removeowner('hopefullythisnotavalidtoken', channel1['channel_id'], user1['u_id'])
    #test invalid id channel
    with pytest.raises(InputError) as e:
        channel_removeowner(user1['token'], channel1['channel_id'] + 10, user1['u_id'])
    #test remove owner when user2 is not owner
    with pytest.raises(InputError) as e:
        channel_removeowner(user1['token'], channel1['channel_id'], user2['u_id'])
    #test remove owner when user2 treis to remove user1
    with pytest.raises(AccessError) as e:
        channel_removeowner(user2['token'], channel1['channel_id'], user1['u_id'])

    channel_addowner(user1['token'], channel1['channel_id'], user2['u_id'])
    #checking that the owners are user1 and user2
    user1_profile = user_profile(user1['token'], user1['u_id'])
    assert details['owner_members'][0]['name_first'] == user1_profile['user']['name_first']

    user2_profile = user_profile(user2['token'], user2['u_id'])
    assert details['owner_members'][1]['name_first'] == user2_profile['user']['name_first']
    assert len(details['owner_member']) == 2

    channel_removeowner(user2['token'], channel1['channel_id'], user2['user_id'])
    #check that after removing the user2 as owner there is only one owner
    assert len(details['owner_members']) == 1

    # test if function gives AccessError when invalid token passed
    with pytest.raises(AccessError) as e:
        channels_create('hopefullythisisnotavalidtoken', 'a', True)

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

def test_channel_leave():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    #Test that when inputed invalid token access error is raised
    with pytest.raises(AccessError) as e:
        channel_leave('hopefullythisnotavalidtoken', channel['channel_id'])
    #test inputerror with an invalid channel_id
    with pytest.raises(InputError) as e:
        channel_leave(user['token'], channel['channel_id'] + 10)
    #test inputerror with invalid channel_id again
    with pytest.raises(InputError) as e:
        channel_leave(user['token'], channel['channel_id'] + 1)
    #test Access error when user is not memeber of channel
    with pytest.raises(AccessError) as e:
        channel_leave(user2['token'], channel['channel_id'])

    details = channel_details(user['token'], channel['channel_id'])
    #make sure the only memeber is the person who created it 
    assert len(details['all_members']) == 1
    channel_leave(user['token'], channel['channel_id'])
    assert len(details['all_members']) == 0

def test_channel_join():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    user2 = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    channel = channels_create(user['token'], 'valid_channel', False)
    
    #Test that when inputed invalid token access error is raised
    with pytest.raises(AccessError) as e:
        channel_join('hopefullythisnotavalidtoken', channel['channel_id'])
    
    #test input error when the channel id is invalid
    with pytest.raises(InputError) as e:
        channel_join(user['token'], channel['channel_id'] + 10)
    
    #test access error when the channel is private and user2 is not admin
    with pytest.raises(AccessError) as e:
        channel_join(user2['token'], channel['channel_id'])
    
    #test join of a public channel
    channel2 = channels_create(user2['token'], 'Public Channel', True)
    details = channel_details(user2['token'], channel2['channel_id'])
    assert len(details['all_members']) == 1
    #test there are now 2 people in the channel
    channel_join(user['u_id'], channel2['u_id'])
    assert len(details['all_members']) == 2
    
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
