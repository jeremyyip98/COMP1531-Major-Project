import pytest
from message import message_send, message_remove, message_edit
from auth import auth_register, auth_login, auth_logout
from channels import channels_create
from channel import channel_join, channel_addowner
from error import InputError
from error import AccessError

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'' test_send_exceed_characters(), test_has_not_joined_channel()
'' The test functions for the message_send function in message.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# If message is more than 1000 characters, InputError
def test_send_exceed_characters():
    results = auth_register("test@gmail.com", "Password", "First", "Last")  # Generate a token

    channelInfo = channels_create(results['token'], 'Cool Kids', False)     # Create a channel and store the channel ID
    with pytest.raises(InputError) as e:
        message_send(results['token'], channelInfo['channel_id'], 'a' * 1001)   # Send a message with more than 1000 characters

# If the authorised user has not joined the channel they are trying to post to, Access Error
def test_has_not_joined_channel(): 
    joined = auth_register("test@gmail.com", "Password", "First", "Last")   # Generate a token that is going to be used
    not_joined = auth_register("notjoined@gmail.com", "Password", "First", "Last")  # Generate a token that is not going to be used

    channelInfo = channels_create(joined['token'], 'Cool Kids', False)  # Create a channel and store the channel ID
    channel_join(joined['token'], channelInfo)                          # Given the stored channel ID, add the user to that channel
    with pytest.raises(AccessError) as e:
        message_send(not_joined['token'], channelInfo['channel_id'], 'abc') # Send a message that the authorised user has not joined that channel


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'' test_remove_not_exists, test_remove_invalid_user()
'' The test functions for the message_remove function in message.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# If the message (based on ID) no longer exists, InputError
def test_remove_not_exists():
    results = auth_register("test@gmail.com", "Password", "First", "Last")  # Generate a token

    channelInfo = channels_create(results['token'], 'Cool Kids', False)     # Create a channel and store the channel ID
    channel_join(results['token'], channelInfo)                             # Given the stored channel ID, add the user to that channel

    messageInfo = message_send(results['token'], channelInfo['channel_id'], 'abc')  # Send a message to the stored channel ID and store the message ID
    message_remove(results['token'], messageInfo)  # Given the stored message ID, remove the message from the channel
    with pytest.raises(InputError) as e:
        message_remove(results['token'], messageInfo)   # Remove the same message again

# If the authorised user is not the one who sent the message, and not an admin/owner of the channel, Access Error
def test_remove_invalid_user():
    results = auth_register("test@gmail.com", "Password", "First", "Last")  # Generate a token
    invalid = auth_register("invalid@gmail.com", "Password", "First", "Last")   # Generate a token

    channelInfo = channels_create(results['token'], 'Cool Kids', False)     # Create a channel and store the channel ID
    channel_join(results['token'], channelInfo)                             # Given the stored channel ID, add the user to that channel
    channel_join(invalid['token'], channelInfo)                             # Add another user to the channel
    channel_addowner(results['token'], channelInfo, results['u_id'])        # Make user of "results" an owner of this channel

    messageInfo = message_send(results['token'], channelInfo['channel_id'], 'abc')  # Send a message to the stored channel ID and store the message ID
    with pytest.raises(AccessError) as e:
        message_remove(invalid['token'], messageInfo)   # Remove a message that was not sent by the given authorised user here
                                                        # In other words, user of "results" is the user who sent the message, but user of "invalid" is trying to remove the message instead
                                                        # Moreover, user of "invalid" is not an owner of this channel

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'' test_edit_invalid_user()
'' The test functions for the message_edit function in message.py
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# If the authorised user is not the one who sent the message, and not an admin/owner of the channel, Access Error
def test_edit_invalid_user():
    results = auth_register("test@gmail.com", "Password", "First", "Last")  # Generate a token
    invalid = auth_register("invalid@gmail.com", "Password", "First", "Last")   # Generate a token

    channelInfo = channels_create(results['token'], 'Cool Kids', False)     # Create a channel and store the channel ID
    channel_join(results['token'], channelInfo)                             # Given the stored channel ID, add the user to that channel
    channel_join(invalid['token'], channelInfo)                             # Add another user to the channel
    channel_addowner(results['token'], channelInfo, results['u_id'])        # Make user of "results" an owner of this channel

    messageInfo = message_send(results['token'], channelInfo['channel_id'], 'abc')  # Send a message to the stored channel ID and store the message ID
    with pytest.raises(AccessError) as e:
        message_edit(invalid['token'], messageInfo, 'abcdefg')      # Edit a message that was not sent by the given authorised user here
                                                                    # In other words, user of "results" is the user that sent the message, but user of "invalid" is trying to ediot the message instead
                                                                    # Moreover, user of "invalid" is not an owner of this channel
