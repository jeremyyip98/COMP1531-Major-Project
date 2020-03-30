"""
UNSW Comp1531 Iteration 2
user HTTP test
Jeffrey Yang z5206134
"""
import json
import json
import requests
import urllib
import pytest

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_user_profile_valid():     
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password ",
            "name_first" : "First",
            "name_last" : "Last"
        }).json() 
    queryString = urllib.parse.urlencode({
                'token' : received['token'] ,
                'u_id' : received['u_id']
            })
    r = requests.get(f"{BASE_URL}/user/profile?{queryString}")
    payload = r.json()
    assert payload['user']['email'] == 'test@gmail.com'
    assert payload['user']['handle_str'] == 'firstlast'
    assert payload['user']['name_first'] == 'First'
    assert payload['user']['name_last'] == 'Last'

def test_user_profile_setname_valid():
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password ",
            "name_first" : "First",
            "name_last" : "Last"
        }).json()
    requests.post(f"{BASE_URL}/user/profile/setname", json={
        "token" : received["token"],
        "name_first" : "Newfirst",
        "name_last" : "Newlast"
    }) 
    queryString = urllib.parse.urlencode({
                'token' : received['token'] ,
                'u_id' : received['u_id']
            })
    r = requests.get(f"{BASE_URL}/user/profile?{queryString}")
    payload = r.json()
    assert payload['user']['email'] == 'test@gmail.com'
    assert payload['user']['handle_str'] == 'firstlast'
    assert payload['user']['name_first'] == 'Newfirst'
    assert payload['user']['name_last'] == 'Newlast'

def test_user_profile_setemail_valid():
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password ",
            "name_first" : "First",
            "name_last" : "Last"
        }).json()
    requests.post(f"{BASE_URL}/user/profile/setemail", json={
        "token" : received["token"],
        "email" : "newtest@gmail.com"
    }) 
    queryString = urllib.parse.urlencode({
                'token' : received['token'] ,
                'u_id' : received['u_id']
            })
    r = requests.get(f"{BASE_URL}/user/profile?{queryString}")
    payload = r.json()
    assert payload['user']['email'] == 'newtest@gmail.com'
    assert payload['user']['handle_str'] == 'firstlast'
    assert payload['user']['name_first'] == 'First'
    assert payload['user']['name_last'] == 'Last'

def test_user_profile_sethandle_valid():
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password ",
            "name_first" : "First",
            "name_last" : "Last"
        }).json()
    requests.post(f"{BASE_URL}/user/profile/sethandle", json={
        "token" : received["token"],
        "handle_str" : "newfirstlast"
    }) 
    queryString = urllib.parse.urlencode({
                'token' : received['token'] ,
                'u_id' : received['u_id']
            })
    r = requests.get(f"{BASE_URL}/user/profile?{queryString}")
    payload = r.json()
    assert payload['user']['email'] == 'test@gmail.com'
    assert payload['user']['handle_str'] == 'newfirstlast'
    assert payload['user']['name_first'] == 'First'
    assert payload['user']['name_last'] == 'Last'
