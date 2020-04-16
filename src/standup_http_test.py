"""
UNSW Comp1531 Iteration 2
user HTTP test
Jeffrey Yang z5206134
"""
import json
import requests
import urllib
import pytest

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_standup_valid():
    #first register user
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password ",
            "name_first" : "First",
            "name_last" : "Last"
        }).json()

    #then create channel
    c_id = requests.post(f"{BASE_URL}/channels/create", json={
        "token" : received['token'],
        "chanel_name" : "test_channel",
        "is_public" : True,
    }).json()

    #then test standup/start
    #then test standup/send (while standup active)
    #then test standup/active (while standup active)
