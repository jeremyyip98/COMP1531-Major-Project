from error import AccessError, InputError
from auth import auth_register
from channels import *
from channel import *
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
    assert channelList['channels'][1]['channel_id'] != channel2['channel_id']
#check if channel1 is a dict or the u_id that it says it returns
    details = channel_details(user1['token'], channel1['channel_id'])
    assert details['name'] = channelList['channels'][0]['name']

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
    
    #test if the channel tries to add channel_id 10231 (invalid id)
    with pytest.raises(InputError) as e:
        channel_addowner(user1['token'], 10231, user1['u_id'])
    
    #invites user2 to channel
    channel_invite(user1['token'],channel1['channel_id'], user2['u_id'])

    #test if the unauthorises user tries to add himself as owner
    with pytest.raises(AccessError) as e:
        channel_addowner(user2['token'], channel1['channel_id'], user2['u_id'])
    
    #adds user2 as owner
    channel_addowner(user1['token'], channel1['channel_id'], user2['u_id'])

    details = channel_details(user2['u_id'], channel1['channel_id'])
    #assert that user 2 is in owners
    user2_profile == user_profile(user2['token'], user2['u_id'])
    assert details['owner_members'][1]['name_first'] == user2_profile['user']['name_first']

def test_channel_details():
    
    






    

    

        
    