""" 
UNSW Comp1531 Iteration 2
Channel HTTP test
Jackie Cai z5259449
"""

import json
import urllib.request
from urllib.error import HTTPError
import pytest

BASE_URL = "http://127.0.0.1:10033"

def test_echo_success():
    response = urllib.request.urlopen('http://127.0.0.1:8080/echo?data=hi')
    payload = json.load(response)
    assert payload['data'] == 'hi'

def test_echo_failure():
    with pytest.raises(HTTPError):
        response = urllib.request.urlopen('http://127.0.0.1:8080/echo?data=echo')

def test_channels_create():
    data = json.dumps({
        'channel_id' : '1',
        'channel_name' : 'My Channel',
        'is_public' : True,
        'owner_members' : ['Jackie'],
        'all_members' : ['Jackie']
    }).encode('utf-8')   
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
