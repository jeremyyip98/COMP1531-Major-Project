""" auth.py contains register, login and logout funcions.
    It imports the registored user store from databse and updates the data there
    to register and authenticate users
"""
#pylint: disable= anomalous-backslash-in-string

import re
import smtplib
import hashlib
import secrets
from error import InputError
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
    return re.search(regex, email)


def generate_u_id():
    '''
    Returns a generated user id

    Returns:
        (int) new u_id: last u_id + 1
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
    '''
    Returns a unique generated token:

    (str) token: 20 character long random url safe string
    '''
    token = secrets.token_urlsafe(20)
    while database.search_database(token):
        token = secrets.token_urlsafe(20)
    return token

def encrypt(password):
    '''
    Encrypts a password

    Paramater:
        password (str): > 6 long password

    Returns:
        (str) sha256 hashed password
    '''
    return hashlib.sha256(password.encode()).hexdigest()

def search_for_email(email):
    '''
    Returns whether email is registered to any users

    Paramater:
        email (str): the email searched for

    Returns:
        (bool) Whether email is registered
    '''
    return any(d['email'] == email for d in database.registered_users_store['registered_users'])

def auth_register(email, password, name_first, name_last):
    '''
    Function which handles registering a user. Checks that all inputs meet specifications and
    throws Input Errors if incorrect. Then generates a token (logging the user in) and handle,
    encrypts the password then adds all information to registered user store.

    Parameters:
        email (str): user's email address
        password (str): password that user types into field
        name_first (str): user's first name
        name_last (str): user's last name

    Returns:
        (dict) with keys u_id and token
    '''
    if not valid_email(email):
        raise InputError(description='Invalid Email address')
    if len(password) < 6 or len(password) > 50:
        raise InputError(description='Password must be between 6 and 50 characters')
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='First name must be between 1 and 50 characters')
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='Last name must be between 1 and 50 characters')
    if database.registered_users_store['registered_users'] and search_for_email(email):
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
        'pwd_reset_code' : False,
        'profile_img_url': ''
        }
    database.registered_users_store['registered_users'].append(user)
    return {'u_id' : u_id, 'token' : token}



def auth_login(email, password):
    '''
    Logs in a user by generating and storing an authentication token for them.

    Parameters:
        email (str): user's email address
        password (str): the user's password

    Returns:
        (dict) with keys u_id and token
    '''
    if not valid_email(email):
        raise InputError(description='Invalid Email address')
    if not search_for_email(email):
        raise InputError(description='Email is not registered to any user')
    for user in database.registered_users_store['registered_users']:
        if user['email'] == email:
            if user['hash'] == encrypt(password):
                if not user['token']:
                    user['token'] = generate_token()
                return {'u_id' : user['u_id'], 'token' : user['token']}
            else:
                raise InputError(description='Incorrect Password')





def auth_logout(token):
    '''
    Logs out a user by deleting their token.

    Paramters:
        token (str): the token belonging to the user logging out

    Returns:
        (bool) Whether the user was successfully logged out
    '''
    is_valid = database.search_database(token)
    if is_valid is False:
        return False
    database.search_database(token)['token'] = False
    return True

def auth_reset_password_request(email):
    '''
    Given an email address generates a unique code, stores it in the user's dictionary
    to which the email belongs to then calls send email.
    This code can then be used to reset the user's password.
    Reset code length determined by PWD_RESET_CODE_LENGTH

    Parameter:
        email (str): the user's email address

    Returns:
        (bool) whether email is registered to any user
    '''
    if not search_for_email(email):
        return False
    code = secrets.token_urlsafe(PWD_RESET_CODE_LENGTH)
    while any(d['pwd_reset_code'] == code\
        for d in database.registered_users_store['registered_users']):
        code = secrets.token_urlsafe(PWD_RESET_CODE_LENGTH)
    for user in database.registered_users_store['registered_users']:
        if user['email'] == email:
            user['pwd_reset_code'] = code
            name = user['name_first']
    
    send_reset_email(email, code, name)

def send_reset_email(to_email, code, name):
    '''
    Formats a message using the code and user's name then sends it in an email

    Parameters:
        to_email (str): the email recipient
        code (str): generated password reset code
        name (str): the user's name to add it to the message
    '''
    subject = "Slackr - Password Reset"
    text = f"""Hi {name},
    Your requested password reset code is "{code}"."""
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (SUPPORT_EMAIL, to_email, subject, text)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(SUPPORT_EMAIL, SUPPORT_EMAIL_PASSWORD)
    server.sendmail(SUPPORT_EMAIL, to_email, message)
    server.close()



def auth_reset_password_reset(reset_code, password):
    '''
    Check an input reset code against the database. If it matches, the new password is
    encrypted and stored as the new hash otherwise input error.

    Parametes:
        reset_code (str): password reset code user gets from email
        password (str): user's chosen new password (>6 characters)
    '''
    if len(password) < 6 or len(password) > 50:
        raise InputError(description='Password must be between 6 and 50 characters')
    for user in database.registered_users_store['registered_users']:
        if user['pwd_reset_code'] == str(reset_code):
            user['hash'] = encrypt(password)
            return
    raise InputError(description='Reset code is invalid')


if __name__ == "__main__":
    pass
