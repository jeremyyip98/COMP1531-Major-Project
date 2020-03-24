import re
import hashlib
import secrets
from error import InputError, AccessError
import database

def valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex,email):
        return True
    else:
        return False

def generate_u_id():
    u_id = max(database.u_ids)
    u_id += 1
    database.u_ids.append(u_id)
    return u_id

def make_handle(first, last):
    first = (first.lower())
    last = last.lower()
    return (first + last)[:20]

def generate_token():
    return secrets.token_urlsafe(15)

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

def search_for_email(email):
    return any(d['email'] == email for d in database.registered_users_store['registered_users'])

def auth_register(email, password, name_first, name_last):
    if not valid_email(email):
         raise InputError(description='Invalid Email address')
    elif len(password) < 6 or len(password) > 50:
        raise InputError(description='Password must be between 6 and 50 characters')
    elif len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='First name must be between 1 and 50 characters')
    elif len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='Last name must be between 1 and 50 characters')
    elif len(database.registered_users_store['registered_users']) > 0 and search_for_email(email):
        raise InputError(description='Email is already in use')
    else:
        token = generate_token()
        u_id = generate_u_id()
        user = {
                'u_id' : u_id,
                'email' : email,
                'name_first' : name_first,
                'name_last' : name_last,
                'hash' : encrypt(password),
                'token' : token,
                'handle_str' : make_handle(name_first, name_last)
                }
        # Will probably implement jwt
        database.registered_users_store['registered_users'].append(user)
        return {'u_id' : u_id, 'token' : token}


def auth_login(email, password):
    if not valid_email(email):
        raise InputError(description='Invalid Email address')
    elif not search_for_email(email):
        raise InputError(description='Email is not registered to any user')
    for d in database.registered_users_store['registered_users']:
        if d['email'] == email:
            if d['hash'] == encrypt(password):
                return {'u_id' : d['u_id'], 'token' :d ['token']}
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