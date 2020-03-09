from auth import auth_register, auth_login, auth_logout
from helper_functions import register_valid_user
import pytest
from error import InputError, AccessError

# Uses register_valid_user function which returns the u_id and

# Checks that registration works
def test_register_valid():
    register_valid_user()

# Email is not a valid address
def test_register_invalid_email():    
    with pytest.raises(InputError) as e:
        auth_register("Invalid_Email", "Password", "First", "Last")    

# Password is too short
def test_register_invalid_password():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Short", "First", "Last")

# Password is too long
# Assumes maximum password is 50
def test_register_too_long_password():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "F"*51, "First", "Last")

def test_register_already_registered_email():
    register_valid_user()
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password1", "First1", "Last1")

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
    details = register_valid_user()
    assert user_profile(details["token"], details["u_id"])["handle_str"] == "firstlast"

# Tests that if first and last name concatenation is more than 20 characters it is cut off at 20 correctly
def test_register_long_handle_concatenation():
    details = auth_register("test@gmail.com", "Password", "VeryLongFirst", "VeryLonglast")
    assert user_profile(details["token"], details["u_id"])["handle_str"] == "verylongfirstverylon"


# Testing successful login
def test_login_valid_details():
    details1 = register_valid_user()
    details2 = auth_login("test@gmail.com", "Password")
    assert details1 == details2


# Logging in with unregistered email
def test_login_invalid_email():
    with pytest.raises(InputError) as e:
        auth_login("bumpkin@gmail.com", "Password")

# Logging in with the wrong password and right password for a registered account
def test_login_wrong_password():
    register_valid_user()
    with pytest.raises(InputError) as e:
        auth_login("test@gmail.com", "WrongPassword")

# Log out a valid user with a valid token
def test_logout_valid_token():
    register_valid_user()
    details = auth_login("test@gmail.com", "Password")
    assert auth_logout(details["token"])["is_success"] == True

# Logs out an invalid token
# Assumes that it is not a valid token
def test_logout_invalid_token():
     with pytest.raises(AccessError) as e:
        auth_logout("hopefullythisisnotavalidtoken")


# Attempts to log out a valid user who is not logged in
# Assume that this should return false
def test_logout_logged_out_user():
    details = register_valid_user()
    auth_logout(details["token"])
    assert auth_logout(details["token"])["is_success"] == False





# Successful login -- Checks that user_id is correctly maintained
# Uses logout function
def test_login_valid_details():
    register_valid_user()
    details1 = auth_login("test@gmail.com", "Password")
    auth_logout(details1["token"])
    details2 = auth_login("test@gmail.com", "Password")
    assert details1["u_id"] == details1["u_id"]
