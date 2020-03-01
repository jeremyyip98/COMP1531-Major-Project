from auth import auth_register
from auth import auth_login
from auth import auth_logout
import pytest
from error import InputError

def test_register_valid():
    auth_register("test@gmail.com", "Password", "First", "Last")

def test_register_invalid_email():    
    with pytest.raises(InputError) as e:
        auth_register("Invalid_Email", "Password", "First", "Last")    

def test_register_invalid_password():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Short", "First", "Last")


def test_register_already_registered_email():
    auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password1", "First1", "Last1")

def test_register_empty_first_name():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password", "", "Last")

def test_register_empty_last_name():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password", "First", "")

def test_register_long_first_name():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password", "F" * 51, "Last")

def test_register_long_last_name():
    with pytest.raises(InputError) as e:
        auth_register("test@gmail.com", "Password", "First", "L" * 51)



def test_login_valid_details():
    auth_register("test@gmail.com", "Password", "First", "Last")
    details1 = auth_login("test@gmail.com", "Password")
    details2 = auth_login("test@gmail.com", "Password")
    assert details1["u_id"] == details1["u_id"]

def test_login_invalid_email():
    with pytest.raises(InputError) as e:
        auth_login("bumpkin@gmail.com", "Password")

def test_login_wrong_password():
    auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        auth_login("test@gmail.com", "WrongPassword")

def test_logout_valid_token():
    auth_register("test@gmail.com", "Password", "First", "Last")
    details = auth_login("test@gmail.com", "Password")
    assert auth_logout(details["token"])["is_success"] == True

# Assumes that it is not a valid token
def test_logout_invalid_token():
     assert auth_logout("hopefullythisisnotavalidtoken")["is_success"] == False

