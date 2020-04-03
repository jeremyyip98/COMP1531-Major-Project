""" 
UNSW Comp1531 Iteration 2
Channel HTTP test
Jackie Cai z5259449
"""
import urllib.request
import json
import requests
from database import get_list_of_channels

BASE_URL = "http://127.0.0.1:8080"
# Helper Functions
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
# ----------------

def test_channels_createt_payload():
    list = get_list_of_channels()
    create_user1()
    payload = requests.post(f"{BASE_URL}/channels/create", json={
        'token' : user1['token'],
        'name' : 'My Channel',
        'is_public' : True,
    })
    assert payload.json() == {'channel_id' : 1}

def test_channels_createf_payload():
    create_user2()
    payload = requests.post(f"{BASE_URL}/channels/create", json={
        'token' : user2['token'],
        'name' : 'False Channel',
        'is_public' : False,
    })
    assert payload.json() == {'channel_id': 2}

def test_list_payload():
    queryString = urllib.parse.urlencode({
        'token' : user1['token'],
    })
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/channels/list?{queryString}"))
    assert payload['channels'] == [{
        'channel_id' : 1,
        'channel_name' : 'My Channel',
    }]

def test_listall_payload():
    queryString = urllib.parse.urlencode({
        'token' : user2['token'],
    })
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/channels/listall?{queryString}"))
    assert payload['channels'] == [{
        'channel_id' : 1,
        'channel_name' : 'My Channel'
        }, {
            'channel_id' : 2,
            'channel_name' : 'False Channel'
        }]
    
def test_join_payload():
    requests.post(f"{BASE_URL}/channel/join", json={
        'token' : user2['token'],
        'channel_id' : 1
    })
    list = get_list_of_channels()
    for i in list['channels']:
        if i['channel_id'] == 1:
            assert user2['u_id'] in i['all_members']

def test_leave_payload():
    requests.post(f"{BASE_URL}/channel/leave", json={
        'token' : user2['token'],
        'channel_id' : 1
    })
    list = get_list_of_channels()
    for i in list['channels']:
        if i['channel_id'] == 1:
            assert user2['u_id'] not in ['all_members']

def test_addowner_payload():
    requests.post(f"{BASE_URL}/channel/addowner", json={
        'token' : user1['token'],
        'channel_id' : 1,
        'u_id' : user2['u_id']
    })
    list = get_list_of_channels()
    for i in list['channels']:
        if i['channel_id'] == 1:
            assert user2['u_id'] in ['owner_members']

def test_removeowner_payload():
    requests.post(f"{BASE_URL}/channel/removeowner", json={
        'token' : user1['token'],
        'channel_id' : 1,
        'u_id' : user2['u_id']
    })
    list = get_list_of_channels()
    for i in list['channels']:
        if i['channel_id'] == 1:
            assert user2['u_id'] not in ['owner_members']
    requests.post(f"{BASE_URL}/workspace/reset", json={})
