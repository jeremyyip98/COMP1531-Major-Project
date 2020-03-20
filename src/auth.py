import re
import hashlib
import secrets

# Set for testing purposes
global u_id_counter
u_id_counter = 1

# Should this be added to server? Made global?
registered_users_store = {
                            'registered_users' : 
                                [
                                    {
                                        'email' : ''
                                    }    
                                ],
                            'hashes': 
                                [
                                    {

                                    }
                                ]
                        }

def valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):
        return True
    else:
        return False  

def make_handle(first, last):
    first = (first.lower())
    last = last.lower()
    return (first + last)[:20]

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_u_id():
    u_id = u_id_counter
    u_id_counter += 1
    return u_id


def auth_register(email, password, name_first, name_last):
    if not valid_email(email):
         raise InputError(description='Invalid Email address')
    elif len(password) < 6 or len(password) > 50:
        raise InputError(description='Password must be between 6 and 50 characters')
    elif len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='First name must be between 1 and 50 characters')
    elif len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='Last name must be between 1 and 50 characters')
    elif any(d['email'] == email for d in registered_users_store['registered_users']):
        raise InputError(description='Email is already in use')
    else:
        user = {
                'u_id' : generate_u_id(),
                'email' : email,
                'name_first' : name_first,
                'name_last' : name_last,
                'password' : encrypt(password),
                'handle_str' : make_handle(name_first, name_last)
                }
        # Will probably implement jwt
        token = secrets.token_urlsafe(15)
        login_info = {
                     'email' : email,
                     'hash' : encrypt(password),
                     'token' : token       
                    }
        
        registered_users_store['registered_users']['users'].append(user)
        registered_users_store['registered_users']['hashes'].append(login_info)
        return token


def auth_login(email, password):
    
    return {'u_id' : 12764, 'token' : 124}

def auth_logout(token):
    return {'is_success':2}

