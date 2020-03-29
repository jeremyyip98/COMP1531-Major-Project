""" auth.py contains register, login and logout funcions.
    It imports the registored user store from databse and updates the data there
    to register and authenticate users
"""

import re
import hashlib
import secrets
from error import InputError, AccessError
import database

def valid_email(email):
    """ Takes email address string and returns true if it is a valid email
    by the method in the spec else returns false """
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        return False

def generate_u_id():
    """ Generates highest u_id + one returns it and appends to u_id list """
    u_id = max(database.u_ids)
    u_id += 1
    database.u_ids.append(u_id)
    return u_id

def make_handle(first, last):
    """ Returns first and last name lower case and concatenated """
    first = (first.lower())
    last = last.lower()
    return (first + last)[:20]

def generate_token():
    token = secrets.token_urlsafe(20)
    print(database.search_database(token))
    while database.search_database(token):
        token = secrets.token_urlsafe(15)
    return secrets.token_urlsafe(15)

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

def search_for_email(email):
    return any(d['email'] == email for d in database.registered_users_store['registered_users'])

def auth_register(email, password, name_first, name_last):
    if not valid_email(email):
        raise InputError(description='Invalid Email address')
    if len(password) < 6 or len(password) > 50:
        raise InputError(description='Password must be between 6 and 50 characters')
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='First name must be between 1 and 50 characters')
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='Last name must be between 1 and 50 characters')
    if len(database.registered_users_store['registered_users']) > 0 and search_for_email(email):
        raise InputError(description='Email is already in use')
    token = generate_token()
    u_id = generate_u_id()
    user = {
        'u_id' : u_id,
        'email' : email,
        'name_first' : name_first,
        'name_last' : name_last,
        'hash' : encrypt(password),
        'token' : token,
        'handle_str' : make_handle(name_first, name_last),
        'permission_id' : 2
        }
    # Will probably implement jwt
    database.registered_users_store['registered_users'].append(user)
    return {'u_id' : u_id, 'token' : token}


#Should logging in wnile logged in do something
def auth_login(email, password):
    if not valid_email(email):
        raise InputError(description='Invalid Email address')
    if not search_for_email(email):
        raise InputError(description='Email is not registered to any user')
    for d in database.registered_users_store['registered_users']:
        if d['email'] == email:
            if d['hash'] == encrypt(password):
                return {'u_id' : d['u_id'], 'token' : d['token']}
            else:
                raise InputError(description='Incorrect Password')


def auth_logout(token):
    is_valid = database.search_database(token)
    if is_valid == False:
        return False
    else:
        database.search_database(token)['token'] = False
        return True



if __name__ == "__main__":
    pass  
