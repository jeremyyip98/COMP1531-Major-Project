"""
UNSW Comp1531 Iteration 2
user HTTP test
Jeffrey Yang z5206134
"""
import json
import urllib
import requests
import pytest

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_user_profile_valid():
    '''We consider the case where we register a user and then show their profile'''
    #reset the workspace
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    #register a user
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password ",
        "name_first" : "First",
        "name_last" : "Last"
    }).json()
    query_string = urllib.parse.urlencode({
        'token' : received['token'],
        'u_id' : received['u_id']
    })
    #get the profile of the registered user
    req = requests.get(f"{BASE_URL}/user/profile?{query_string}")
    payload = req.json()
    assert payload['user']['email'] == 'test@gmail.com'
    assert payload['user']['handle_str'] == 'firstlast'
    assert payload['user']['name_first'] == 'First'
    assert payload['user']['name_last'] == 'Last'

def test_user_profile_setname_valid():
    '''We register a user and try changing their name'''
    #reset the workspace
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    #register a user
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password ",
        "name_first" : "First",
        "name_last" : "Last"
    }).json()
    #change the user's name
    requests.post(f"{BASE_URL}/user/profile/setname", json={
        "token" : received["token"],
        "name_first" : "Newfirst",
        "name_last" : "Newlast"
    })
    query_string = urllib.parse.urlencode({
                'token' : received['token'],
                'u_id' : received['u_id']
    })
    #check if the user's name has been changed
    req = requests.get(f"{BASE_URL}/user/profile?{query_string}")
    payload = req.json()
    assert payload['user']['email'] == 'test@gmail.com'
    assert payload['user']['handle_str'] == 'firstlast'
    assert payload['user']['name_first'] == 'Newfirst'
    assert payload['user']['name_last'] == 'Newlast'

def test_user_profile_setemail_valid():
    '''We register a user and try changing their email'''
    #reset the workspace
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password ",
        "name_first" : "First",
        "name_last" : "Last"
    }).json()
    #change the user's email
    requests.post(f"{BASE_URL}/user/profile/setemail", json={
        "token" : received["token"],
        "email" : "newtest@gmail.com"
    })
    query_string = urllib.parse.urlencode({
        'token' : received['token'],
        'u_id' : received['u_id']
    })
    #check if the email has been changed
    req = requests.get(f"{BASE_URL}/user/profile?{query_string}")
    payload = req.json()
    assert payload['user']['email'] == 'newtest@gmail.com'
    assert payload['user']['handle_str'] == 'firstlast'
    assert payload['user']['name_first'] == 'First'
    assert payload['user']['name_last'] == 'Last'

def test_user_profile_sethandle_valid():
    '''We register a user and change their handle'''
    #reset the workspace
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password ",
        "name_first" : "First",
        "name_last" : "Last"
    }).json()
    #change the user's handle
    requests.post(f"{BASE_URL}/user/profile/sethandle", json={
        "token" : received["token"],
        "handle_str" : "newfirstlast"
    })
    query_string = urllib.parse.urlencode({
        'token' : received['token'],
        'u_id' : received['u_id']
    })
    #check if the handle has been changed
    req = requests.get(f"{BASE_URL}/user/profile?{query_string}")
    payload = req.json()
    assert payload['user']['email'] == 'test@gmail.com'
    assert payload['user']['handle_str'] == 'newfirstlast'
    assert payload['user']['name_first'] == 'First'
    assert payload['user']['name_last'] == 'Last'
