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

def test_channel_list():
#test if the channel list returns id 1 and the name 'my channel'
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    channelList = channels_list(user1['token'])
    assert channelList['channel_id'] == channel1['channel_id']
    assert channelList['name'] == 'My Channel'

def test_channel_list_all():
#same as channel_list but add one more channel
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    channelList = channels_listall(user1['token'])
    assert channelList['channel_id'] == channel1['channel_id']
    assert channelList['name'] == 'My Channel'

def test_channel_addowner():
    #assume user1 is owner of channel when he makes the channel
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('anme2@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)

    #test if the channel adds user1 again it gives InputError
    with pytest.raises(InputError) as e:
        channel_addowner(user1['token'], channel1['channel_id'], user1['u_id'])
    
    #test if the channel tries to add channel_id 2 (invalid id)
    with pytest.raises(InputError) as e:
        channel_addowner(user1['token'], 2, user1['u_id'])
    
    #invites user2 to channel
    channel_invite(user1['token'],channel1['channel_id'], user2['u_id'])

    #test if the unauthorises user tries to add himself as owner
    with pytest.raises(AccessError) as e:
        channel_addowner(user2['token'], channel1['channel_id'], user2['u_id'])
    
    #adds user2 as owner
    channel_addowner(user1['token'], channel1['channel_id'], user2['u_id'])

    details = channel_details(user2['u_id'], channel1['channel_id'])
    #assert that user 2 is in owners
    assert user2['u_id'] in details['owner_members']

def test_channel_invite_errors():
    user = auth.register('name@mail.com', 'password', 'John', 'Doe')
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
    user2 = auth.register('name2@mail.com', 'passw0rd', 'Ben', 'Ny')
    with pytest.raises(AccessError) as e:
         channel_invite(user['token'], channel['channel_id'], user2['u_id'])





    

    

        
    
