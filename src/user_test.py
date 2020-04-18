'''
COMP1531
User function tests
Jeffrey Yang
'''
import pytest
import database
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from helper_functions import register_valid_user, register_another_valid_user
from error import InputError, AccessError

# We assume that auth_register works

def test_user_profile_valid():
    ''' For a valid user, the returned profile should match with the details of the user '''
    database.restore_database()
    results = register_valid_user()
    profile = user_profile(results["token"], results["u_id"])["user"]
    assert profile["u_id"] == results["u_id"]
    assert profile["email"] == "test@gmail.com"
    assert profile["name_first"] == "First"
    assert profile["name_last"] == "Last"
    assert profile["handle_str"] == "firstlast"


def test_user_profile_invalid_token():
    ''' We raise an access error since we passed in an invalid token '''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(AccessError) as e:
        user_profile("hopefullythisisnotavalidtoken", results["u_id"])


def test_user_profile_invalid_user():
    ''' User with u_id has to be a valid user
    We raise an input error since the u_id is invalid '''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(InputError) as e:
        user_profile(results["token"], 999)

# We now assume that user_profile works


def test_user_profile_setname_valid():
    '''Both name_first and name_list need to be strings between 1 and 50 characters in length
    We assume that u_id, email and handle_str are not affected '''
    database.restore_database()
    results = register_valid_user()
    user_profile_setname(results["token"], "Newfirst", "Newlast")
    profile = user_profile(results["token"], results["u_id"])["user"]
    assert profile["u_id"] == results["u_id"]
    assert profile["email"] == "test@gmail.com"
    assert profile["name_first"] == "Newfirst"
    assert profile["name_last"] == "Newlast"
    assert profile["handle_str"] == "firstlast"


def test_user_profile_setname_invalid_token():
    ''' We raise an access error since we passed in an invalid token '''
    database.restore_database()
    with pytest.raises(AccessError) as e:
        user_profile_setname("hopefullythisisnotavalidtoken", "Newfirst", "Newlast")


def test_user_profile_setname_first_name_too_short():
    ''' Here, the new name_first is too short '''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(InputError) as e:
        user_profile_setname(results["token"], "", "NewLast")


def test_user_profile_setname_first_name_too_long():
    ''' Here, the new name_first is too long '''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(InputError) as e:
        user_profile_setname(results["token"], "a"*51, "Newlast")


def test_user_profile_setname_last_name_too_short():
    ''' Here, the new name_last is too short '''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(InputError) as e:
        user_profile_setname(results["token"], "NewFirst", "")


def test_user_profile_setname_last_name_too_long():
    ''' Here, the new name_last is too long '''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(InputError) as e:
        user_profile_setname(results["token"], "NewFirst", "b"*51)


def test_user_profile_setemail_valid():
    ''' The new email has to be valid and cannot be already used by another user
    We assume that u_id, name_first, name_last and handle_str are not affected '''
    database.restore_database()
    results = register_valid_user()
    user_profile_setemail(results["token"], "newtest@gmail.com")
    profile = user_profile(results["token"], results["u_id"])["user"]
    assert profile["u_id"] == results["u_id"]
    assert profile["email"] == "newtest@gmail.com"
    assert profile["name_first"] == "First"
    assert profile["name_last"] == "Last"
    assert profile["handle_str"] == "firstlast"


def test_user_profile_setemail_invalid_token():
    ''' We raise an access error since we passed in an invalid token '''
    database.restore_database()
    with pytest.raises(AccessError) as e:
        user_profile_setemail("hopefullythisisnotavalidtoken", "newtest@gmail.com")


def test_user_profile_setemail_invalid():
    ''' Here, the new email is invalid '''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(InputError) as e:
        user_profile_setemail(results["token"], "invalidemail")


def test_user_profile_setemail_email_already_used():
    ''' Here, the new email is already being used by another user '''
    database.restore_database()
    results = register_valid_user()
    results2 = register_another_valid_user()
    profile2 = user_profile(results2["token"], results2["u_id"])["user"]
    with pytest.raises(InputError) as e:
        user_profile_setemail(results["token"], profile2["email"])


def test_user_profile_sethandle_valid():
    ''' handle_str must be between 3 and 20 characters and cannot be already used by another user
    We assume that u_id, email, name_first and name_last are not affected '''
    database.restore_database()
    results = register_valid_user()
    user_profile_sethandle(results["token"], "newhandle")
    profile = user_profile(results["token"], results["u_id"])["user"]
    assert profile["u_id"] == results["u_id"]
    assert profile["email"] == "test@gmail.com"
    assert profile["name_first"] == "First"
    assert profile["name_last"] == "Last"
    assert profile["handle_str"] == "newhandle"


def test_user_profile_sethandle_invalid_token():
    ''' We raise an access error since we passed in an invalid token'''
    database.restore_database()
    with pytest.raises(AccessError) as e:
        user_profile_sethandle("hopefullythisisnotavalidtoken", "newhandle")


def test_user_profile_sethandle_handle_too_short():
    '''Here, the new handle_str is too short'''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(InputError) as e:
        user_profile_sethandle(results["token"], "a")


def test_user_profile_sethandle_handle_too_long():
    '''Here, the new handle_str is too long'''
    database.restore_database()
    results = register_valid_user()
    with pytest.raises(InputError) as e:
        user_profile_sethandle(results["token"], "a"*21)


def test_user_profile_sethandle_handle_already_used():
    ''' Here, the new handle is already being used by another user '''
    database.restore_database()
    results = register_valid_user()
    results2 = register_another_valid_user()
    profile2 = user_profile(results2["token"], results2["u_id"])["user"]
    with pytest.raises(InputError) as e:
        user_profile_sethandle(results["token"], profile2["handle_str"])
        