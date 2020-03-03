from error import AccessError, InputError
from auth import auth_register
from channels import *
import pytest


def test_channel_create():
#test if there is an input error when character string is greater than 20
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    with pytest.raises(InputError) as e:
        channels_create(user1['token'], 'a' * 21, True)

def test_channel_list():
#test if the channel list returns id 1 and the name 'my channel'
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    channels_create(user1['token'], 'My Channel', True)
    channelList = channels_list(user1['token'])
    assert channelList['channel_id'] == 1
    assert channelList['name'] == 'My Channel'

def test_channel_list_all():
#same as channel_list but add one more channel
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    channels_create(user1['token'], 'My Channel', True)
    channelList = channels_listall(user1['token'])
    assert channelList['channel_id'] == 1
    assert channelList['name'] == 'My Channel'


    

        
    