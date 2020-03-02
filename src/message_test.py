import pytest
from message import message_send, message_remove, message_edit
from auth import auth_register, auth_login, auth_logout
from channels import channels_create
from error import InputError
from error import AccessError

# Testing a valid amount of characters of message
def test_send_valid_characters():
    results = auth_register("test@gmail.com", "Password", "First", "Last")

    channelInfo = channels_create(results['token'], 'Cool Kids', False)
        messge_send(result['token'], channelInfo['channel_id'], 'abc')

# If message is more than 1000 characters, InputError
def test_send_exceed_characters():
    results = auth_register("test@gmail.com", "Password", "First", "Last")

    channelInfo = channels_create(results['token'], 'Cool Kids', False)
    with pytest.raises(InputError) as e:
        messge_send(result['token'], channelInfo['channel_id'], 'a' * 1001)

# If the token is not valid, AccessError (assumption)
def test_send_invalid_token():
    channelInfo = channels_create(results['token'], 'Cool Kids', False)
    with pytest.raises(AccessError) as e:
        messge_send('invalid_token', channelInfo['channel_id'], 'abc') # Assume this is an invalid token



# If the authorised user has not joined the channel they are trying to post to, Access Error
def test_has_not_joined_channel(): 


def test_remove():


def test_edit():