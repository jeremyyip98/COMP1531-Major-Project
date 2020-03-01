import auth
import pytest
from error import InputError

def test_register_same_details():
    details1 = auth.auth_register("test@gmail.com", "Password", "First", "Last")
    details2 = auth.auth_register("test@gmail.com", "Password", "First", "Last")
    assert details1["u_id"] == details1["u_id"]
    assert details1["token"] == details1["token"]    

def test_login_same_details():
    details1 = auth.auth_login("test@gmail.com", "Password")
    details2 = auth.auth_login("test@gmail.com", "Password")
    assert details1["u_id"] == details1["u_id"]
    assert details1["token"] == details1["token"]

