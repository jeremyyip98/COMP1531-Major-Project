"""
auth_http_test.py
This file is written by Sean McCaughey
"""
import json
import urllib
import pytest
import requests

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"


def register_example_use():
    """This funciton test for the user register for example use"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    return received

def test_register_valid():
    """This function test if thes register valid or not"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password",
        "name_first" : "First",
        "name_last" : "Last"
    }).json()
    query_string = urllib.parse.urlencode({
                'token' : received['token'],
                'u_id' : received['u_id']
    })
    res = requests.get(f"{BASE_URL}/user/profile?{query_string}")
    payload = res.json()['user']
    assert payload['email'] == 'test@gmail.com'
    assert payload['name_first'] == 'First'




def test_register_invalid_password():
    """This function test for registering an invalid password"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "short",
        "name_first" : "First",
        "name_last" : "Last"
    })
    assert payload.status_code == 400



# Password is too long
# Assumes maximum password is 50
def test_register_too_long_password():
    """This funciton test for a user registering with a long password"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "F"*51,
        "name_first" : "First",
        "name_last" : "Last"
    })
    assert payload.status_code == 400

def test_register_already_registered_email():
    """This function test for an email that have already been registered"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password",
        "name_first" : "First",
        "name_last" : "Last"
    })
    assert received.status_code == 400


def test_register_empty_first_name():
    """This function test for a user trying to register with empty first name"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "F"*51,
        "name_first" : "",
        "name_last" : "Last"
    })
    assert payload.status_code == 400

def test_register_empty_last_name():
    """This function test for a user trying to register with empty last name"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "F"*51,
        "name_first" : "First",
        "name_last" : ""
    })
    assert payload.status_code == 400

def test_register_too_long_first_name():
    """This function test for a user trying to register with a very long first name"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "First",
        "name_first" : "First"*51,
        "name_last" : "Last"
    })
    assert payload.status_code == 400

def test_register_too_long_last_name():
    """This function test for a user trying to register with a very long last name"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "First",
        "name_first" : "First",
        "name_last" : "Last"*51
    })
    assert payload.status_code == 400


# The tests involving handles assume that user_profile works correctly
def test_register_handle_correct():
    """This function test for the handle_str works correctly"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password",
        "name_first" : "First",
        "name_last" : "Last"
    }).json()
    query_string = urllib.parse.urlencode({
                'token' : received['token'],
                'u_id' : received['u_id']
    })
    res = requests.get(f"{BASE_URL}/user/profile?{query_string}").json()
    payload = res['user']
    assert payload['handle_str'] == 'firstlast'


# Tests that if first and last name concatenation is more
# than 20 characters it is cut off at 20 correctly
def test_register_long_handle_concatenation():
    """This function test a register with long handle concatenation"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "Password",
        "name_first" : "VeryLongFirst",
        "name_last" : "VeryLonglast"
    }).json()
    query_string = urllib.parse.urlencode({
                'token' : received['token'],
                'u_id' : received['u_id']
    })
    res = requests.get(f"{BASE_URL}/user/profile?{query_string}")
    payload = res.json()['user']
    assert payload['handle_str'] == "verylongfirstverylon"

def test_login_valid():
    """This function test if the login valid or not"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    register_example_use()
    payload = requests.post(f"{BASE_URL}/auth/login", json={
        "email" : "test@gmail.com",
        "password" : "Password"
    })
    assert payload.status_code == 200



# Logging in with unregistered email
def test_login_invalid_email():
    """This function test to login with an invalid email"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    assert requests.post(f"{BASE_URL}/auth/login", json={
        "email" : "bumpkin@gmail.com",
        "password" : "Password"
        }).status_code == 400

# Logging in with the wrong password and right password for a registered account
def test_login_wrong_password():
    """This function test login with a wrong password"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    register_example_use()
    assert requests.post(f"{BASE_URL}/auth/login", json={
        "email" : "test@gmail.com",
        "password" : "wrongpassword"
        }).status_code == 400


# Log out a valid user with a valid token
def test_logout_valid_token():
    """This function test logout with a valid token"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    details = register_example_use().json()
    received = requests.post(f"{BASE_URL}/auth/logout", json={"token" :details['token']}).json()
    assert received['is_success'] is True

# Logs out an invalid token
# Assumes that it is not a valid token
def test_logout_invalid_token():
    """This function test logout with an invalid token"""
    received = requests.post(f"{BASE_URL}/auth/logout", json={"token" : 'notavalidtoken'})
    assert received.json()['is_success'] is False
    assert received.status_code == 200

# Attempts to log out a valid user who is not logged in
# Assume that this should return false
def test_logout_logged_out_user():
    """This function test to logout with a user that already been logout"""
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    details = register_example_use().json()
    received = requests.post(f"{BASE_URL}/auth/logout", json={"token" :details['token']}).json()
    assert received['is_success'] is True
    received = requests.post(f"{BASE_URL}/auth/logout", json={"token" :details['token']})
    assert received.json()['is_success'] is False
    assert received.status_code == 200
