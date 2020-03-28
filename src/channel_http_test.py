""" 
UNSW Comp1531 Iteration 2
Channel HTTP test
Jackie Cai z5259449
"""

import json
import urllib.request
from database import restore_channel_database, restore_database

BASE_URL = "http://127.0.0.1:8080"

def test_channels_createt_payload():
    data = json.dumps({
        'token' : 'validtoken',
        'channel_name' : 'My Channel',
        'is_public' : True,
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload['token'] == 'validtoken'
    assert payload['channel_name'] == 'My Channel'
    assert payload['is_public'] is True

def test_channels_createf_payload():
    data = json.dumps({
        'token' : 'validtoken2',
        'channel_name' : 'False Channel',
        'is_public' : False,
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload['token'] == 'validtoken2'
    assert payload['channel_name'] == 'False Channel'
    assert payload['is_public'] is False

def test_list_payload():
    queryString = urllib.parse.urlencode({
        'token' : 'validtoken',
    })
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/channels/list?{queryString}"))
    assert payload['channels'] == [{
        'channel_id' : 1,
        'channel_name' : 'My Channel',
    }]

def test_listall_payload():
    queryString = urllib.parse.urlencode({
        'token' : 'validtoken2',
    })
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/channels/listall?{queryString}"))
    assert payload['channels'] == [{
        'channel_id' : 1,
        'channel_name' : 'My Channel'
        }, {
            'channel_id' : 2,
            'channel_name' : 'False Channel'
        }]
    restore_channel_database()
    restore_database()

def test_join_payload():
    data = json.dumps({
        'token' : 'validtoken',
        'channel_id' : 1,
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))  
    assert payload['token'] == 'validtoken'
    assert payload['channel_id'] == 1
    restore_channel_database()
    restore_database()  

def test_leave_payload():
    data = json.dumps({
        'token' : 'validtoken',
        'channel_id' : 1,
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/leave", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))  
    assert payload['token'] == 'validtoken'
    assert payload['channel_id'] == 1
    restore_channel_database()
    restore_database()

def test_addowner_payload():
    data = json.dumps({
        'token' : 'validtoken',
        'channel_id' : 1,
        'u_id' : 1,
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))  
    assert payload['token'] == 'validtoken'
    assert payload['channel_id'] == 1
    assert payload['u_id'] == 1
    restore_channel_database()
    restore_database()

def test_removeowner_payload():
    data = json.dumps({
        'token' : 'validtoken',
        'channel_id' : 1,
        'u_id' : 1,
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))  
    assert payload['token'] == 'validtoken'
    assert payload['channel_id'] == 1
    assert payload['u_id'] == 1
    restore_channel_database()
    restore_database()
