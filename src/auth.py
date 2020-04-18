""" auth.py contains register, login and logout funcions.
    It imports the registored user store from databse and updates the data there
    to register and authenticate users
"""

import re
import smtplib
import hashlib
import secrets
from error import InputError, AccessError
import database

PWD_RESET_CODE_LENGTH = 6
SUPPORT_EMAIL = "flying.circus.slackr@gmail.com"
SUPPORT_EMAIL_PASSWORD = "wF79s@5qbEQp" 

def valid_email(email):
    '''
    Returns whether email is as valid email according to spec

    Parameter:
        email (str): email address

    Returns:
        (bool) Whether or not email is valid format
    '''
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        return False

def generate_u_id():
    '''
    Returns a generated user id

    Returns:
        (int) u_id: last u_id + 1
    '''
    u_id = max(database.u_ids)
    u_id += 1
    database.u_ids.append(u_id)
    return u_id

def make_handle(first, last):
    '''
    Returns first and last name lower case and concatenated and cut off
    at 20 characters for use as handle

    Parameters:
        first (str): firt name
        last (str): last name

    Returns:
        handle (str)
    '''


    first = (first.lower())
    last = last.lower()
    return (first + last)[:20]

def generate_token():
    token = secrets.token_urlsafe(20)
    while database.search_database(token):
        token = secrets.token_urlsafe(15)
    return token

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
        'permission_id' : 1 if u_id == 1 else 2,
        'hash' : encrypt(password),
        'token' : token,
        'handle_str' : make_handle(name_first, name_last),
        'pwd_reset_code' : False
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
                if not d['token']:
                    d['token'] = generate_token()
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

def auth_reset_password_request(email):
    if not search_for_email(email):
        return False
    # Check that its unique
    
    code = secrets.token_urlsafe(PWD_RESET_CODE_LENGTH)
    while any(d['pwd_reset_code'] == code for d in database.registered_users_store['registered_users']):
        code = secrets.token_urlsafe(PWD_RESET_CODE_LENGTH)


    for d in database.registered_users_store['registered_users']:
        if d['email'] == email:
            d['pwd_reset_code'] = code
            name = d['name_first']
    send_reset_email(email, code, name)

def send_reset_email(to_email, code, name):
    SUBJECT = "Slackr - Password Reset"
    TEXT = f"""Hi {name},
    Your requested password reset code is "{code}"."""
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (SUPPORT_EMAIL, to_email, SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(SUPPORT_EMAIL, SUPPORT_EMAIL_PASSWORD)
    server.sendmail(SUPPORT_EMAIL, to_email, message)   
    server.close()



def auth_reset_password_reset(reset_code, password):
    if len(password) < 6 or len(password) > 50:
        raise InputError(description='Password must be between 6 and 50 characters')
    for user in database.registered_users_store['registered_users']:
        if user['pwd_reset_code'] == str(reset_code):
            user['hash'] = encrypt(password)
        else:
            raise InputError(description='Reset code is invalid')
    

if __name__ == "__main__":
    pass
