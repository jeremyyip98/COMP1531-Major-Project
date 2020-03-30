import json
import requests
import urllib
import pytest

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"


def register_example_use():
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password",
            "name_first" : "First",
            "name_last" : "Last"
        })
    return received

def test_register_valid():
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password",
            "name_first" : "First",
            "name_last" : "Last"
        }).json() 
    queryString = urllib.parse.urlencode({
                'token' : received['token'] ,
                'u_id' : received['u_id']
            })
    r = requests.get(f"{BASE_URL}/user/profile?{queryString}")
    payload = r.json()['user']
    assert payload['email'] == 'test@gmail.com'
    assert payload['name_first'] == 'First'




def test_register_invalid_password():
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
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "F"*51,
        "name_first" : "First",
        "name_last" : "Last"
    })
    assert payload.status_code == 400

def test_register_already_registered_email():  
    requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password ",
            "name_first" : "First",
            "name_last" : "Last"
        })
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password ",
            "name_first" : "First",
            "name_last" : "Last"
        })
    assert received.status_code == 400
    

def test_register_empty_first_name():
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "F"*51,
        "name_first" : "",
        "name_last" : "Last"
    })
    assert payload.status_code == 400

def test_register_empty_last_name():
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "F"*51,
        "name_first" : "First",
        "name_last" : ""
    })
    assert payload.status_code == 400

def test_register_too_long_first_name():
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "First",
        "name_first" : "First"*51,
        "name_last" : "Last"
    })
    assert payload.status_code == 400

def test_register_too_long_last_name():
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "First",
        "name_first" : "First",
        "name_last" : "Last"*51
    })
    assert payload.status_code == 400


# The tests involving handles assume that user_profile works correctly
def test_register_handle_correct():  
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
    r = requests.get(f"{BASE_URL}/user/profile?{queryString}").json()
    payload = r['user']
    assert payload['handle_str'] == 'firstlast'


# Tests that if first and last name concatenation is more than 20 characters it is cut off at 20 correctly
def test_register_long_handle_concatenation():
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password ",
            "name_first" : "VeryLongFirst",
            "name_last" : "VeryLonglast"
        }).json() 
    queryString = urllib.parse.urlencode({
                'token' : received['token'] ,
                'u_id' : received['u_id']
            })
    r = requests.get(f"{BASE_URL}/user/profile?{queryString}")
    payload = r.json()['user']
    assert payload['handle_str'] == "verylongfirstverylon"

def test_login_valid():
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    register_example_use()
    payload = requests.post(f"{BASE_URL}/auth/login", json={
        "email" : "test@gmail.com",
        "password" : "Password"
    })
    assert payload.status_code == 200



# Logging in with unregistered email
def test_login_invalid_email():
    assert requests.post(f"{BASE_URL}/auth/login", json={
        "email" : "bumpkin@gmail.com",
        "password" : "Password"
        }).status_code == 400

# Logging in with the wrong password and right password for a registered account
def test_login_wrong_password():
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    register_example_use() 
    assert requests.post(f"{BASE_URL}/auth/login", json={
        "email" : "test@gmail.com",
        "password" : "wrongpassword"
        }).status_code == 400


# Log out a valid user with a valid token
def test_logout_valid_token():
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    details = register_example_use().json()
    received = requests.post(f"{BASE_URL}/auth/logout", json={"token" :details['token'] }).json() 
    assert received['is_success'] == True

# Logs out an invalid token
# Assumes that it is not a valid token
def test_logout_invalid_token():
    received = requests.post(f"{BASE_URL}/auth/logout", json={"token" : 'notavalidtoken' })
    assert received.json()['is_success'] == False
    assert received.status_code == 200

# Attempts to log out a valid user who is not logged in
# Assume that this should return false
def test_logout_logged_out_user():
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    details = register_example_use().json()
    received = requests.post(f"{BASE_URL}/auth/logout", json={"token" :details['token'] }).json() 
    assert received['is_success'] == True
    received = requests.post(f"{BASE_URL}/auth/logout", json={"token" :details['token'] }) 
    assert received.json()['is_success'] == False
    assert received.status_code == 200



