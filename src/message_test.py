"""
UNSW COMP1531 Project Iteration 2
message_test.py
Written by: Yip Jeremy Chung Lum, z5098112
"""
import pytest
from database import reset_message, restore_channel_databse, restore_database, reset_channel, get_message
from message import message_send, message_remove, message_edit
from channel import channel_join, channel_addowner, channel_messages
from channels import channels_create
from helper_functions import register_valid_user, register_another_valid_user
from error import InputError, AccessError

def restore_everything():
    """This function restore everything and return nothing"""
    reset_message()
    restore_channel_databse()
    restore_database()
    reset_channel()

#########################################################
# The test functions for the message_send() in message.py
#########################################################
def test_send_exceed_characters():
    """This function raise InputError, if message is more than 1000 characters"""
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)
    with pytest.raises(InputError):
        # Send a message with more than 1000 characters
        message_send(results['token'], channel_info, 'a' * 1001)

def test__send_not_joined_channel():
    """This function raise AccessError, if the authorised user has not joined
    the channel they are trying to post to"""
    restore_everything()
    # Generate a token that is going to be used
    joined = register_valid_user()

    # Generate a token that is not going to be used
    not_joined = register_another_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(joined['token'], 'Cool Kids', False)

    with pytest.raises(AccessError):
        # Send a message that the authorised user has not joined that channel
        message_send(not_joined['token'], channel_info, 'abc')

def test_send_correct_channel():
    """This function check if the message was sent to the channel"""
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)

    # Send a message
    message_id = message_send(results['token'], channel_info, 'abc')

    message_list = get_message()

    # Initialising channel_message
    channel_message = 'something'

    for msg_dict in message_list:
        if msg_dict['message_id'] == message_id:
            channel_message = msg_dict['message']

    assert channel_message == 'abc'

def test_send_invalid_token():
    """This function check if it's an invalid token"""
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)
    with pytest.raises(AccessError):
        message_send('hopefullythisisnotavalidtoken', channel_info, 'abc')

###########################################################
# The test functions for the message_remove() in message.py
###########################################################
def test_remove_not_exists():
    """This function raise InputError, if the message (based on ID) no longer exist"""
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)

    # Send a message to the stored channel ID and store the message ID
    message_info = message_send(results['token'], channel_info, 'abc')

    # Given the stored message ID, remove the message from the channel
    message_remove(results['token'], message_info)

    with pytest.raises(InputError):
        # Remove the same message again
        message_remove(results['token'], message_info)

def test_remove_invalid_user():
    """This function rais AccessError, if the authorised user is not the one who sent the message,
     and not an admin/owner of the channel"""
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Generate a token
    not_owner = register_another_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)

    # Add another user to the channel
    channel_join(not_owner['token'], channel_info)

    # Make user of "results" an owner of this channel
    channel_addowner(results['token'], channel_info, results['u_id'])

    # Send a message to the stored channel ID and store the message ID
    message_info = message_send(results['token'], channel_info, 'abc')

    with pytest.raises(AccessError):
        message_remove(not_owner['token'], message_info)
        # Remove a message that was not sent by the given authorised user here
        # In other words, user of "results" is the user who sent the message,
        # but user of "invalid" is trying to remove the message instead
        # Moreover, user of "invalid" is not an owner of this channel

def test_remove_confirm():
    """This function check if the message was removed in the channel"""
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)

    # Make user of "results" an owner of this channel
    channel_addowner(results['token'], channel_info, results['u_id'])

    # Send a message to the stored channel ID
    message_send(results['token'], channel_info, 'abc')

    # Send another message
    message_info2 = message_send(results['token'], channel_info, 'hellomate')

    # Remove the recent messsage
    message_remove(results['token'], message_info2)

    # Store the most recent message in the channel
    output = channel_messages(results['token'], channel_info, 0)

    # Get the list "messages" from the dictionary "output"
    channel_list = output.get('messages')

    # Get the first index in the list, which is a dictionary
    channel_dict = channel_list[0]

    # Get the key "message" from the dictionary
    channel_message = channel_dict.get('message')

    assert channel_message == 'abc'


def test_remove_invalid_token():
    """This function check if it's an invalid token"""
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)

    # Send a message to the stored channel ID and store the message ID
    message_info = message_send(results['token'], channel_info, 'abc')
    with pytest.raises(AccessError):
        message_remove('hopefullythisisnotavalidtoken', message_info)

###########################################################
# The test functions for the message_edit() in message.py
###########################################################
def test_edit_invalid_user():
    """This function return AccessErrori f the authorised user is not the one who sent the message,
    and not an admin/owner of the channel """
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Generate a token
    not_owner = register_another_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)

    # Add another user to the channel
    channel_join(not_owner['token'], channel_info)

    # Make user of "results" an owner of this channel
    channel_addowner(results['token'], channel_info, results['u_id'])

    # Send a message to the stored channel ID and store the message ID
    message_info = message_send(results['token'], channel_info, 'abc')
    with pytest.raises(AccessError):
        message_edit(not_owner['token'], message_info, 'abcdefg')
        # Edit a message that was not sent by the given authorised user here
        # In other words, user of "results" is the user that sent the message,
        # but user of "invalid" is trying to ediot the message instead
        # Moreover, user of "invalid" is not an owner of this channel

def test_edit_confirm():
    """This function check if the message was edtied in the channel"""
    restore_everything()
    # Generate a token
    results = register_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)

    # Make user of "results" an owner of this channel
    channel_addowner(results['token'], channel_info, results['u_id'])

    # Send a message to the stored channel ID and store the message ID
    message_info = message_send(results['token'], channel_info, 'abc')

    # Edit a message
    message_edit(results['token'], message_info, 'abcdefg')

    # Store the most recent message in the channel
    output = channel_messages(results['token'], channel_info, 0)

    # Get the list "messages" from the dictionary "output"
    channel_list = output.get('messages')

    # Get the first index in the list, which is a dictionary
    channel_dict = channel_list[0]

    # Get the key "message" from the dictionary
    channel_message = channel_dict.get('message')

    assert channel_message == 'abcdefg'

def test_edit_invalid_token():
    """This function check if it's an invalid token"""
    restore_everything()
      # Generate a token
    results = register_valid_user()

    # Create a channel and store the channel ID
    channel_info = channels_create(results['token'], 'Cool Kids', False)

    # Send a message to the stored channel ID and store the message ID
    message_info = message_send(results['token'], channel_info, 'abc')
    with pytest.raises(AccessError):
        message_edit('hopefullythisisnotavalidtoken', message_info, 'abcdefg')
