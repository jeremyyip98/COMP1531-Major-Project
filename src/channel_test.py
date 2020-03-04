from error import AccessError, InputError
from auth import auth_register
from channels import *
from channel import *
from user import user_profile
import pytest


def test_channel_create():
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
    channelList = channels_list(user1['token'])
    
    assert channelList['channels'][0]['channel_id'] == channel1['channel_id']
    assert len(channelList['channels']) == 1

    details = channel_details(user1['token'], channel1['channel_id'])
    assert details['name'] == channelList['channels'][0]['name']

    channelList2 = channels_list(user2['token'])
    
    assert channelList2['channels'][0]['channel_id'] == channel2['channel_id']
    assert len(channelList2['channels']) == 1

    details = channel_details(user2['token'], channel2['channel_id'])
    assert details['name'] == channelList2['channels'][0]['name']

def test_channel_listall():
#when called the channel list all should list all channels including id and name regardless
#if the user is in the channel or not (assuming thats what specs says)
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name2@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    channel2 = channels_create(user2['token'],'Second Channel', False)
    channelList = channels_listall(user1['token'])

    assert channelList['channels'][0]['channel_id'] == channel1['channel_id']
    assert channelList['channels'][1]['channel_id'] == channel2['channel_id']


def test_channel_addowner():
    #assume user1 is owner of channel when he makes the channel
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name2@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)

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
    #assert that user 2 is in owners
    user2_profile = user_profile(user2['token'], user2['u_id'])
    assert details['owner_members'][1]['name_first'] == user2_profile['user']['name_first']

def test_channel_remove_owner():
    #assume user1 is owner of channel when he makes the channel
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name2@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    details = channel_details(user1['u_id'], channel1['channel_id'])

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
    #check that after removing the person the second 
    assert len(details['owner_members']) == 1


def test_channel_invite_errors():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    
### test when inviting user to a channel with invalid channel_id - gives InputError
    # u_id is valid
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'] + 1, user['u_id'])
    # testing same issue with a separate but invalid channel_id
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'] + 10, user['u_id'])
        
### test when inviting an invalid u_id - gives InputError
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user['u_id'] + 1)
    # testing same issue with a separate but invalid u_id
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user['u_id'] + 10)
        
### test when a non-member of channel invites another user
    user2 = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    user3 = auth_register('name3@mail.com', 'password1', 'Tim', 'He')
    with pytest.raises(AccessError) as e:
         channel_invite(user2['token'], channel['channel_id'], user2['u_id'])

#Test that the function works
    details = channel_details(user['token'], channel['channel_id'])
    assert len(details['all_members']) == 1

    channel_invite(user['token'], channel['channel_id'], user2['u_id'])
    assert len(details['all_members']) == 2
    
    channel_invite(user3['token'], channel['channel_id'], user3['u_id'])
    assert len(details['all_members']) == 3
#raises input error when the person added is already in channel
    with pytest.raises(InputError) as e:
        channel_invite(user['token'], channel['channel_id'], user2['u_id'])
#make sure the number of memeber stays at 3
    channel_invite(user3['token'], channel['channel_id'], user3['u_id'])
    assert len(details['all_members']) == 3

def test_channel_leave():
    user = auth_register('name@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    user2 = auth_register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    #test inputerror with an invalid channel_id
    with pytest.raises(InputError) as e:
        channel_leave(user['token'], channel['channel_id'] + 10)
    #test inputerror wit invalid channel_id again
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
#test input error when the channel id is invalid
    with pytest.raises(InputError) as e:
        channel_join(user['token'], channel['channel_id'] + 10)
#test access error when the channel is private and user2 is not admin
    with pytest.raises(AccessError) as e:
        channel_join(user2['token'], channel['channel_id'])
        
