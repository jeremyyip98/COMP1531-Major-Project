from other import users_all, search
from auth import auth_register
from helper_functions import register_valid_user, create_valid_channel
from message import message_send
import pytest
from error import InputError

def test_users_all_one_user():
    details = register_valid_user()
    users = users_all(details["token"])
    assert users["users"][0]["name_first"] == "First" 

def test_users_all_two_users():
    details = register_valid_user()
    auth_register("another@gmail.com", "Password", "Second", "Last1")
    users = users_all(details["token"])
    assert users["users"][0]["name_first"] == "First" 
    assert users["users"][1]["name_first"] == "Second"
    
"""
Test for each entry in the dictionary
"""

def send_test_message(message, channel_name):
    channel_id, details = create_valid_channel(channel_name, True)
    message_details = message_send(details["token"], channel_id, message)
    return message_details, details

# Assumes messages are in some sort of order when multiple results

def test_search_one_channel():
    # This registers a user, creates a channel and sends the message and returns the message 
    # detail and the channel creators details
    message_details, details = send_test_message("Test Message", "test_channel_one")
    send_test_message("Different Message", "test_channel_one")
    search_results = search(details["token"], "test")
    # Checks that the message containing "test" is found by the search
    assert search_results["messages"][0]["message_id"] == message_details["message_id"]

def test_search_two_channels():
    pass
