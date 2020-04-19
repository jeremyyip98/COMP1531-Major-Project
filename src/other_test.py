'''
Comp1531 Assignment other_test.py
'''
#pylint: disable = mixed-indentation, invalid-name, trailing-whitespace, unused-variable, line-too-long
#disable unused since we need that for pytest raise error as
#disable line too long since some lines are needed to be long to send long messages to assert they are valid
import pytest
from channels import channels_create
from channel import channel_invite, channel_details
from other import users_all, admin_userpermission_change, search, admin_user_remove
from helper_functions import (register_valid_user,
                              register_another_valid_user,
                              create_admin,
                              create_valid_channel
                             )
from database import restore_database, get_profile_allinfo, registered_users_store
from message import message_send
from error import InputError, AccessError

def test_users_all_invalid_token():
    '''Checks that an invalid token throws Access Error'''
    with pytest.raises(AccessError) as e:
        users_all('hopefullythisisnotavalidtoken')

def test_users_all_one_user():
    '''Testing users all with one user'''
    restore_database()
    details = register_valid_user()
    users = users_all(details["token"])
    assert users["users"][0]["u_id"] == details["u_id"]
    assert users["users"][0]["name_first"] == "First" 
    assert users["users"][0]["name_last"] == "Last" 
    assert users["users"][0]["email"] == "test@gmail.com" 
    assert users["users"][0]["handle_str"] == "firstlast" 

def test_users_all_two_users():
    '''Testing users all with two users'''
    details = register_another_valid_user()
    users = users_all(details["token"])
    assert users["users"][0]["name_first"] == "First" 
    assert users["users"][1]["name_first"] == "Anotherfirst"

def send_test_message(message, channel_name, different_user):
    '''Helper function which creates a user, channel and then sends a message to it'''
    channel_id, details = create_valid_channel(channel_name, different_user)
    message_details = message_send(details["token"], channel_id, message)
    return message_details, details, channel_id

def test_search_invalid_token():
    '''Assumes messages are in some sort of order when multiple results'''
    with pytest.raises(AccessError) as e:
        search('hopefullythisisnotavalidtoken', "irrelevantsearchterm")

def test_search_one_channel():
    '''This registers a user, creates a channel and sends the message and returns the message 
     detail and the channel creators details''' 
    restore_database()
    message_details, details, channel_id = send_test_message("Test Message", "test_channel_one", False)
    print(details)
    message_send(details["token"], channel_id, "A different message")
    search_results = search(details["token"], "test")
    print(search_results)
    # Checks that the message containing "test" is found by the search
    assert search_results["messages"][0]["message_id"] == message_details



def test_search_multiple_channels_and_messages():
    ''' Sends 2 messages where one contains the search term. This is done twice to new channels '''
    restore_database()
    details = register_valid_user()
    channel_id = channels_create(details["token"], "One", True)['channel_id']
    msg_id1 = message_send(details['token'], channel_id, "gobble")
    message_send(details['token'], channel_id, "not this one")
    channel_id = channels_create(details["token"], "Two", True)['channel_id']
    msg_id2 = message_send(details['token'], channel_id, "gobble2")
    message_send(details['token'], channel_id, "not this one either")
    search_results = search(details["token"], "gobble")
    assert any(d["message_id"] == msg_id1 for d in search_results["messages"])
    assert any(d["message_id"] == msg_id2 for d in search_results["messages"])


def test_search_term_in_channel_not_joined():
    '''Sends one message containing the search term to a channel created by different users each. Searches for the term
    with one users token and asserts that only the message from the channel he has joined is found'''
    restore_database()
    user_one = False
    user_two = True
    message_details, details, test = send_test_message("Gobble", "test_channel_one", user_one)
    send_test_message("Gobble", "test_channel_two", user_two)
    assert len(search(details["token"], "gobble")["messages"]) == 3

def test_admin_permission_change_error():
    '''testing errors that shold pop up'''
    restore_database()
    admin = create_admin()
    user = register_another_valid_user()
    #test access error when user is not an admin
    with pytest.raises(AccessError) as err:
        admin_userpermission_change(user['token'], user['u_id'], 1)
    #test input error when permssion id is not 1 or 2
    with pytest.raises(InputError) as err:
    	admin_userpermission_change(admin['token'], user['u_id'], 3)
    #test access error with invalid token
    with pytest.raises(AccessError) as err:
    	admin_userpermission_change('hopefullyinvlaidtoken', user['u_id'], 1)
    #test invalid user token
    with pytest.raises(InputError) as err:
    	admin_userpermission_change(admin['token'], user['u_id'] + 100, 1)
    restore_database()

def test_admin_permission_change_normal():
    '''test the function works properly'''
    admin = create_admin()
    user = register_another_valid_user()
    user = get_profile_allinfo(user['u_id'])
    #make sure the id is from 2 to 1
    assert user['permission_id'] == 2
    admin_userpermission_change(admin['token'], user['u_id'], 1)
    assert user['permission_id'] == 1
    restore_database()

def test_admin_user_remove_error():
    '''test the remove user error should be popping up'''
    admin = create_admin()
    user = register_another_valid_user()
    with pytest.raises(AccessError) as err:
        #test access error with invalid token
        admin_user_remove('hopefullyaninvalidtoken', user['u_id'])
    with pytest.raises(AccessError) as err:
        #test access error when the user is not an admin
        admin_user_remove(user['token'], user['u_id'])
    with pytest.raises(InputError) as err:
        #test when u_id does not refer to valid user
        admin_user_remove(admin['token'], 123)
    restore_database()

def test_admin_user_remove_normal():
    '''test remove user works normally'''
    #make users and then make the channels and add some users
    admin = create_admin()
    user1 = register_another_valid_user()
    user2 = register_valid_user()
    channel = channels_create(user1['token'], 'My Channel', True)
    channel_invite(user1['token'], channel['channel_id'], user2['u_id'])
    details = channel_details(user2['token'], channel['channel_id'])
    #make sure the users are in the database and channels
    assert len(details['all_members']) == 2
    assert len(details['owner_members']) == 1
    assert len(registered_users_store['registered_users']) == 3
    admin_user_remove(admin['token'], user1['u_id'])
    #make sure the person is removed from the channels and user database
    details = channel_details(user2['token'], channel['channel_id'])
    assert len(details['all_members']) == 1
    assert not details['owner_members']
    assert len(registered_users_store['registered_users']) == 2
    restore_database()
