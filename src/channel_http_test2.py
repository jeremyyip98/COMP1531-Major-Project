import json
import urllib.request
import requests
from database import get_message, get_list_of_channels, get_channel

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"

# Helper Functions
'''
u_id:
    user1 u_id = 1
    user2 u_id = 2
'''
def create_user1():
    global user1
    user1 = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'mail@mail.com',
        'password' : 'password',
        'name_first' : 'first',
        'name_last' : 'last'
    })
    user1 = user1.json()
    return user1

def create_user2():
    global user2
    user2 = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'mail2@mail.com',
        'password' : 'password',
        'name_first' : 'first',
        'name_last' : 'last'
    })
    user2 = user2.json()
    return user2
    
def send_message():
    """This function testing the /message/send route and return nothing"""
    requests.delete(f"{BASE_URL}/message/reset")

    payload = requests.post(f"{BASE_URL}/message/send", json={
        "token" : 0,
        "channel_id" : 0,
        "message" : 'abc'
    })
    msg_list = get_message()
    for dict_msg in msg_list:
        if dict_msg['message_id'] == payload['message_id']:
            assert dict_msg['message'] == 'abc'

def create_valid_channel():
    create_user1()
    payload = requests.post(f"{BASE_URL}/channels/create", json={
        'token' : user1['token'],
        'name' : 'My Channel',
        'is_public' : True,
    })
    details = payload.json()
    return details['channel_id']
    
def join_channel(user, channel_id):
    requests.post(f"{BASE_URL}/channel/join", json={
        'token' : user['token'],
        'channel_id' : channel_id
    })
    channel_list = get_list_of_channels()
    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            assert user['u_id'] in channel['all_members']
    
#-------------------------------------------------------------#
""" HTTP tests """

def test_invite_payload():
    # Resets the workspace
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    create_user1()
    create_user2()
    channel_id = create_valid_channel()
    
    # User1 invites user2 to the channel
    payload = requests.post(f"{BASE_URL}/channel/invite", json={
        'token' : user1['token'],
        'channel_id' : channel_id,
        'u_id' : 2
    })
    
    channel_list = get_list_of_channels()
    for channel in channel_list:
        if channel['channel_id'] == channel_id:
            assert user2['u_id'] in channel['all_members']
    
def test_details_payload():
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    create_user1()
    create_user2()
    channel_id = create_valid_channel()
    # add user2 to the channel (user1 is already in the channel since he created it)
    join_channel(user2, channel_id)
    queryString = urllib.parse.urlencode({
        'token' : user1['token'],
        'channel_id' : channel_id})
    
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{queryString}")
    payload = json.load(response)
    
    # user1 is the owner as he created the channel
    owner_list = [{
        'u_id': user1['u_id'],
        'name_first': user1['name_first'],
        'name_last': user1['name_last']
    }]
    
    member_list = [{
        'u_id': user1['u_id'],
        'name_first': user1['name_first'],
        'name_last': user1['name_last']
    },{
        'u_id': user2['u_id'],
        'name_first': user2['name_first'],
        'name_last': user2['name_last']
    }]
    # makes sure the return values for details is correct
    assert payload == {
        'name' : 'My Channel',
        'owner_members' : owner_list,
        'all_members' : member_list
    }
    
def test_message_payload():
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    create_user1()
    channel_id = create_valid_channel()
    
    # sends 10 messages
    for i in range(10):
        send_message()
    
    queryString = urllib.parse.urlencode({
        'token' : user1['token'],
        'channel_id' : channel_id,
        'start' : 0
    })
    
    response = urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}")
    payload = json.load(response)
    
    id_list = []
    # Initialise message and channel list
    msg_list = get_message()
    chan_list = get_channel()
    for channel in chan_list:
        if channel['channel_id'] == channel_id:
            for message_id in channel['channel_messages']:
                id_list.append(message_id)
    
    messages = []
    for ids in id_list:
        for msg_dict in msg_list:
            if msg_dict['message_id'] == ids:
                messages.append(msg_dict)
    
    assert payload == {
        'messages' : messages,
        'start' : 0,
        'end' : -1
    }
    
    # sends 100 messages
    for i in range(100):
        send_message()
    
    queryString = urllib.parse.urlencode({
        'token' : user1['token'],
        'channel_id' : channel_id,
        'start' : 20
    })
    
    response = urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}")
    payload = json.load(response)

    for channel in chan_list:
        if channel['channel_id'] == channel_id:
            for message_id in channel['channel_messages']:
                id_list.append(message_id)
    
    messages = []
    for ids in id_list:
        for msg_dict in msg_list:
            if msg_dict['message_id'] == ids:
                messages.append(msg_dict)
    
    assert payload == {
        'messages' : messages,
        'start' : 20,
        'end' : 70
    }
