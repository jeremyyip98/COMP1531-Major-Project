import pytest
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register
from error import InputError


# We assume that auth_register works


def test_user_profile_valid():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    profile = user_profile(results["token"], results["u_id"])
    assert profile["u_id"] == results["u_id"]
    assert profile["email"] == "test@gmail.com"
    assert profile["name_first"] == "First"
    assert profile["name_last"] == "Last"
    assert profile["handle_str"] == "firstlast"
    
# User with u_id has to be a valid user
def test_user_profile_invalid_user():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile(results["token"], "INVALIDUSER")


def test_user_profile_setname_valid():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    user_profile_setname(results["token"], "Newfirst", "Newlast")

# name_first has to be between 1 and 50 characters in length
def test_user_profile_setname_first_name_too_short():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile_setname(results["token"], "", "Last")

def test_user_profile_setname_first_name_too_long():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile_setname(results["token"], "a"*51, "Newlast")

# name_last has to be between 1 and 50 characters in length
def test_user_profile_setname_last_name_too_short():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile_setname(results["token"], "First", "")

def test_user_profile_setname_last_name_too_long():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile_setname(results["token"], "First", "b"*51)


def test_user_profile_setemail_valid():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    user_profile_setemail(results["token"], "newtest@gmail.com")

# email has to be valid
def test_user_profile_setemail_invalid():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile_setemail(results["token"], "invalidemail")

# new email cannot already be used
def test_user_profile_setemail_email_already_used():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile_setemail(results["token"], "test@gmail.com")


def test_user_profile_sethandle_valid():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    user_profile_sethandle(results["token"], "newHandle")

# handle_str must be between 3 and 20 characters
def test_user_profile_sethandle_handle_too_short():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile_sethandle(results["token"], "a")

def test_user_profile_sethandle_handle_too_long():
    results = auth_register("test@gmail.com", "Password", "First", "Last")
    with pytest.raises(InputError) as e:
        user_profile_sethandle(results["token"], "a"*21)

# new handle cannot already be used
def test_user_profile_sethandle_handle_already_used():
    results = auth_register("test@gmail.com", "Password", "First", "Last") # the handle for this user is "firstlast"
    with pytest.raises(InputError) as e:
        user_profile_sethandle(results["token"], "firstlast")