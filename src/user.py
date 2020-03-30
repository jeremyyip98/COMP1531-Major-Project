from error import InputError
import database
import helper_functions

def user_profile(token, u_id):
    u_id = int(u_id)
    database.check_token(token)
    profile = database.get_profile(u_id)
    return {'user': profile}

def user_profile_setname(token, name_first, name_last):
    database.check_token(token)
    if 1 <= len(name_first) <= 50 and 1 <= len(name_last) <= 50:
        database.set_name(token, name_first, name_last)
        return {}
    if not 1 <= len(name_first) <= 50 and 1 <= len(name_last) <= 50:
        raise InputError(description='First name must be between 1 and 50 characters')
    if 1 <= len(name_first) <= 50 and not 1 <= len(name_last) <= 50:
        raise InputError(description='Last name has to be between 1 and 50 characters in length')
    raise InputError(description='First and last name must be between 1 and 50 characters')

def user_profile_setemail(token, email):
    database.check_token(token)
    if not helper_functions.valid_email(email):
        raise InputError(description='Invalid email address')
    if database.check_email_already_used(email):
        raise InputError(description='Email is already being used by another user')
    database.set_email(token, email)
    return {}

def user_profile_sethandle(token, handle_str):
    database.check_token(token)
    if database.check_handle_str_already_used(handle_str):
        raise InputError(description='Handle is already being used by another user')
    if 2 <= len(handle_str) <= 20:
        database.set_handle(token, handle_str)
        return {}
    raise InputError(description='Handle must be between 2 and 20 characters')
