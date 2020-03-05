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
    # This registers a user, creates a channel and sends the message and returns the message 
    # detail and the channel creators details
    send_test_message("Search term isnt in this message", "test_channel_one")
    message_details, details = send_test_message("Search term is gobble", "test_channel_two")
    
    search_results = search(details["token"], "gobble")
    # Checks that the message containing "test" is found by the search
    assert search_results["messages"][0]["message_id"] == message_details["message_id"]

# Sends three messages to and creates a channel with channel_name. One message contains the search term
def send_three_messages(channel_name):
    send_test_message("Search term isnt in this message", channel_name)
    send_test_message("Nor in this one", channel_name)
    return send_test_message("Search term is gobble", channel_name)
    

def test_search_multiple_channels_and_messages():
    
    message_details1, details = send_three_messages("test_channel_one")
    message_details2 = send_three_messages("test_channel_two")[0]
    message_details3 = send_three_messages("test_channel_two")[0]
    
    search_results = search(details["token"], "gobble")
    # Searches through the list of dictionaries to ensure the message_id containing the search term is 
    # in the search results
    assert any(d["message_id"] == message_details1["message_id"] for d in search_results["messages"])
    assert any(d["message_id"] == message_details2["message_id"] for d in search_results["messages"])
    assert any(d["message_id"] == message_details3["message_id"] for d in search_results["messages"])





