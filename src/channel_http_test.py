"""
UNSW Comp1531 Iteration 2
Channel HTTP test
Jackie Cai z5259449
"""
#pylint: disable=C0103, W0601, C0303
import urllib.request
import json
import requests

BASE_URL = "http://127.0.0.1:10013"
# Helper Functions
def create_user1():
    '''Helper function to make user in server'''
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
    '''Helper function to make user in server'''
    global user2
    user2 = requests.post(f"{BASE_URL}/auth/register", json={
        'email': 'mail2@mail.com',
        'password' : 'password',
        'name_first' : 'Jim',
        'name_last' : 'Slim'
    })
    user2 = user2.json()
    return user2

def create_valid_channel(user):
    '''Helper function to make channel in server'''
    payload = requests.post(f"{BASE_URL}/channels/create", json={
        'token' : user['token'],
        'channel_name' : 'My Channel',
        'is_public' : True,
    })
    return payload.json()['channel_id']

def details_get(token, channel_id):
    '''Helper function to get channel details to check in server'''
    queryString = urllib.parse.urlencode({
        'token' : token,
        'channel_id' : channel_id,
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{queryString}")
    payload = json.load(response)
    return payload
# ----------------

def test_channels_createt_payload():
    '''testing create with true public'''
    create_user1()
    payload = requests.post(f"{BASE_URL}/channels/create", json={
        'token' : user1['token'],
        'name' : 'My Channel',
        'is_public' : True,
    })
    assert payload.json() == {'channel_id' : 1}

def test_channels_createf_payload():
    '''testing create with Flase public'''
    create_user2()
    payload = requests.post(f"{BASE_URL}/channels/create", json={
        'token' : user2['token'],
        'name' : 'False Channel',
        'is_public' : False,
    })
    assert payload.json() == {'channel_id': 2}

def test_list_payload():
    '''Test the list only shows one'''
    queryString = urllib.parse.urlencode({
        'token' : user1['token'],
    })
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/channels/list?{queryString}"))
    assert payload['channels'] == [{
        'channel_id' : 1,
        'name' : 'My Channel',
    }]

def test_listall_payload():
    '''Test listall shows both channels'''
    queryString = urllib.parse.urlencode({
        'token' : user2['token'],
    })
    payload = json.load(urllib.request.urlopen(f"{BASE_URL}/channels/listall?{queryString}"))
    assert payload['channels'] == [{
        'channel_id' : 1,
        'name' : 'My Channel'
        }, {
            'channel_id' : 2,
            'name' : 'False Channel'
        }]
    
def test_join_payload():
    '''test join a public channel'''
    requests.post(f"{BASE_URL}/channel/join", json={
        'token' : user2['token'],
        'channel_id' : 1
    })
    details = details_get(user2['token'], 1)
    owner_list = [{
        'u_id': user1['u_id'],
        'name_first': 'first',
        'name_last': 'last'
    }]
    member_list = [{
        'u_id': user1['u_id'],
        'name_first': 'first',
        'name_last': 'last'
    }, {
        'u_id': user2['u_id'],
        'name_first':'Jim',
        'name_last': 'Slim'
    }]
    assert details == {
        'name' : 'My Channel',
        'owner_members' : owner_list,
        'all_members' : member_list
    }

def test_addowner_payload():
    '''Test add owner to a channel'''
    requests.post(f"{BASE_URL}/channel/addowner", json={
        'token' : user1['token'],
        'channel_id' : 1,
        'u_id' : user2['u_id']
    })
    details = details_get(user2['token'], 1)
    owner_list = [{
        'u_id': user1['u_id'],
        'name_first': 'first',
        'name_last': 'last'
    }, {
        'u_id': user2['u_id'],
        'name_first':'Jim',
        'name_last': 'Slim'
    }]
    member_list = [{
        'u_id': user1['u_id'],
        'name_first': 'first',
        'name_last': 'last'
    }, {
        'u_id': user2['u_id'],
        'name_first':'Jim',
        'name_last': 'Slim'
    }]
    assert details == {
        'name' : 'My Channel',
        'owner_members' : owner_list,
        'all_members' : member_list
    }

def test_removeowner_payload():
    '''Test remove owner'''
    requests.post(f"{BASE_URL}/channel/removeowner", json={
        'token' : user1['token'],
        'channel_id' : 1,
        'u_id' : user2['u_id']
    })
    details = details_get(user2['token'], 1)
    owner_list = [{
        'u_id': user1['u_id'],
        'name_first': 'first',
        'name_last': 'last'
    }]
    member_list = [{
        'u_id': user1['u_id'],
        'name_first': 'first',
        'name_last': 'last'
    }, {
        'u_id': user2['u_id'],
        'name_first':'Jim',
        'name_last': 'Slim'
    }]
    assert details == {
        'name' : 'My Channel',
        'owner_members' : owner_list,
        'all_members' : member_list
    }

def test_leave_payload():
    '''Test leave works and reset channel database'''
    requests.post(f"{BASE_URL}/channel/leave", json={
        'token' : user2['token'],
        'channel_id' : 1
    })
    detail = details_get(user1['token'], 1)
    owner_list = [{
        'u_id': user1['u_id'],
        'name_first': 'first',
        'name_last': 'last'
    }]
    member_list = [{
        'u_id': user1['u_id'],
        'name_first': 'first',
        'name_last': 'last'
    }]
    assert detail == {
        'name' : 'My Channel',
        'owner_members' : owner_list,
        'all_members' : member_list
    }
    requests.post(f"{BASE_URL}/workspace/reset", json={})
