import json
import requests
import urllib
import pytest

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"


def test_register_valid():
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "password",
        "name_first" : "First",
        "name_last" : "Last"
    })




def test_register_invalid_password():
    


# Password is too long
# Assumes maximum password is 50
def test_register_too_long_password():
    payload = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "test@gmail.com",
        "password" : "F"*51,
        "name_first" : "First",
        "name_last" : "Last"
    })

def test_register_already_registered_email():
    restore_database()
    test_register_valid()
    test_register_valid()
    

def test_register_empty_first_name():
    
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password", "", "Last")

def test_register_empty_last_name():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password", "First", "")

def test_register_too_long_first_name():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password", "F" * 51, "Last")

def test_register_too_long_last_name():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password", "First", "L" * 51)



# The tests involving handles assume that user_profile works correctly

# Tests that a handle is correctly concatenated
def test_register_handle_correct():
    restore_database()
    details = register_valid_user()
    assert user_profile(details["token"], details["u_id"])['user']["handle_str"] == "firstlast"

# Tests that if first and last name concatenation is more than 20 characters it is cut off at 20 correctly
def test_register_long_handle_concatenation():
    restore_database()
    details = auth_register("test@gmail.com", "Password", "VeryLongFirst", "VeryLonglast")
    assert user_profile(details["token"], details["u_id"])['user']["handle_str"] == "verylongfirstverylon"

def test_login_valid():
    payload = requests.post(f"{BASE_URL}/auth/login", json={
        "email" : "test@gmail.com",
        "password" : "password"
    })