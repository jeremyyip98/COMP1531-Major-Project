"""
UNSW COMP1531 Project Iteration 2
message_http_test.py
Written by: Yip Jeremy Chung Lum, z5098112
"""
import datetime
import requests
from database import message_list

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_send_valid():
    """This function testing the /message/send route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    req = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    user = req.json()

    res = requests.post(f"{BASE_URL}/channels/create", json={
        "token" : user['token'],
        "channel_name" : "Random Name",
        "is_public" : True
    })
    channel = res.json()

    r = requests.post(f"{BASE_URL}/message/send", json={
        "token" : user['token'],
        "channel_id" : channel['channel_id'],
        "message" : 'abc'
    })
    payload = r.json()

    global message_list
    for dict_msg in message_list:
        if dict_msg['message_id'] == payload['message_id']:
            assert dict_msg['message'] == 'abc'

def test_sendlater_valid():
    """This function test the /message/sendlater route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    req = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    user = req.json()

    res = requests.post(f"{BASE_URL}/channels/create", json={
        "token" : user['token'],
        "channel_name" : "Random Name",
        "is_public" : True
    })
    channel = res.json()

    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(minutes=10)
    timestamp = now_plus_10.replace(tzinfo=datetime.timezone.utc).timestamp()
    r = requests.post(f"{BASE_URL}/message/sendlater", json={
        "token" : user['token'],
        "channel_id" : channel['channel_id'],
        "message" : 'abc',
        "time_sent" : timestamp
    })
    payload = r.json()

    global message_list
    for dict_msg in message_list:
        if dict_msg['message_id'] == payload['message_id']:
            assert dict_msg['time_created'] == timestamp

def test_react_valid():
    """This function test the /message/react route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    req = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    user = req.json()

    res = requests.post(f"{BASE_URL}/channels/create", json={
        "token" : user['token'],
        "channel_name" : "Random Name",
        "is_public" : True
    })
    channel = res.json()

    # send a message
    r = requests.post(f"{BASE_URL}/message/send", json={
        "token" : user['token'],
        "channel_id" : channel['channel_id'],
        "message" : 'abc'
    })
    payload = r.json()

    requests.post(f"{BASE_URL}/message/react", json={
        "token" : user['token'],
        "message_id" : 0,
        "react_id" : 1
    })

    global message_list
    for dict_msg in message_list:
        if dict_msg['message_id'] == payload['message_id']:
            for dict_react in dict_msg['reacts']:
                # Check if the u_ids have something in it
                assert dict_react['u_ids'] is True

def test_unreact_valid():
    """This function test the /message/unreact route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    req = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    user = req.json()
    res = requests.post(f"{BASE_URL}/channels/create", json={
        "token" : user['token'],
        "channel_name" : "Random Name",
        "is_public" : True
    })
    channel = res.json()

    # send a message
    r = requests.post(f"{BASE_URL}/message/send", json={
        "token" : user['token'],
        "channel_id" : channel['channel_id'],
        "message" : 'abc'
    })
    payload = r.json()

    requests.post(f"{BASE_URL}/message/unreact", json={
        "token" : user['token'],
        "message_id" : 0,
        "react_id" : 1
    })

    global message_list
    for dict_msg in message_list:
        if dict_msg['message_id'] == payload['message_id']:
            for dict_react in dict_msg['reacts']:
                # Check if the u_ids empty
                assert dict_react['u_ids'] is False

def test_pin_valid():
    """This function test the /message/pin route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    req = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    user = req.json()

    res = requests.post(f"{BASE_URL}/channels/create", json={
        "token" : user['token'],
        "channel_name" : "Random Name",
        "is_public" : True
    })
    channel = res.json()

    # send a message
    r = requests.post(f"{BASE_URL}/message/send", json={
        "token" : user['token'],
        "channel_id" : channel['channel_id'],
        "message" : 'abc'
    })
    payload = r.json()

    requests.post(f"{BASE_URL}/message/pin", json={
        "token" : user['token'],
        "message_id" : 0,
    })

    global message_list
    for dict_msg in message_list:
        if dict_msg['message_id'] == payload['message_id']:
            # check if the message pinned or not
            assert dict_msg['is_pinned'] is True

def test_unpin_valid():
    """This function test the /message/pin route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    req = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    user = req.json()

    res = requests.post(f"{BASE_URL}/channels/create", json={
        "token" : user['token'],
        "channel_name" : "Random Name",
        "is_public" : True
    })
    channel = res.json()

    # send a message
    r = requests.post(f"{BASE_URL}/message/send", json={
        "token" : user['token'],
        "channel_id" : channel['channel_id'],
        "message" : 'abc'
    })
    payload = r.json()

    requests.post(f"{BASE_URL}/message/unpin", json={
        "token" : user['token'],
        "message_id" : 0,
    })

    global message_list
    for dict_msg in message_list:
        if dict_msg['message_id'] == payload['message_id']:
            # check if the message pinned or not
            assert dict_msg['is_pinned'] is False


def test_remove_valid():
    """This function test the /message/remove route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    req = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    user = req.json()

    # send a message
    test_send_valid()
    requests.delete(f"{BASE_URL}/message/remove", json={
        "token" : user['token'],
        "message_id" : 0,
    })
    global message_list
    # Check if the list empty because we've just removed the one and only one message in the list,
    # which the message_list should back to empty again
    assert message_list == []

def test_edit_valid():
    """This function test the /message/edit route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    req = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    user = req.json()
    res = requests.post(f"{BASE_URL}/channels/create", json={
        "token" : user['token'],
        "channel_name" : "Random Name",
        "is_public" : True
    })
    channel = res.json()

    # send a message
    r = requests.post(f"{BASE_URL}/message/send", json={
        "token" : user['token'],
        "channel_id" : channel['channel_id'],
        "message" : 'abc'
    })
    payload = r.json()

    requests.put(f"{BASE_URL}/message/edit", json={
        "token" : user['token'],
        "message_id" : 0,
        "message" : 'something'
    })

    global message_list
    for dict_msg in message_list:
        if dict_msg['message_id'] == payload['message_id']:
            # check if the message got edit or not
            assert dict_msg['message'] == 'something'
