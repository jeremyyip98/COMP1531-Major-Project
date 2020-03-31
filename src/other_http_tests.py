import json
import requests
import urllib
import pytest

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"


def register_example_user():
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "othertest@gmail.com",
            "password" : "Password",
            "name_first" : "Other",
            "name_last" : "Last"
        })
    return received.json()

def test_users_all():
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    details = register_example_user()
    queryString = urllib.parse.urlencode({'token' : details['token']})
    r = requests.get(f"{BASE_URL}/users/all?{queryString}")
    response = r.json()['users'][0]
    assert response['email'] == 'othertest@gmail.com'
    assert response['name_first'] == 'Other'

def test_users_all_more():
    details = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "anothertest@gmail.com",
            "password" : "Password",
            "name_first" : "Other",
            "name_last" : "Last"
        }).json()
    requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "evenmore@gmail.com",
            "password" : "Password",
            "name_first" : "Other",
            "name_last" : "Last"
        })    
    queryString = urllib.parse.urlencode({'token' : details['token']})
    r = requests.get(f"{BASE_URL}/users/all?{queryString}")
    response = r.json()['users']
    assert response[0]['email'] == 'othertest@gmail.com'
    assert response[1]['email'] == 'anothertest@gmail.com'
    assert response[2]['email'] == 'evenmore@gmail.com'


def create_channel(token):
    channel_id = requests.post(f"{BASE_URL}/channels/create", json={
            "token" : token,
            "channel_name" : "test_channel",
            "is_public" : "True"
        }).json()
    return channel_id['channel_id']
    
def send_message(token, message, channel_id):
    message_id = requests.post(f"{BASE_URL}/message/send", json={
            "token" : token,
            "channel_id" : channel_id,
            "message" : message
        }).json() 
    return message_id['message_id']

def search_messages(token, query_str):
    queryString = urllib.parse.urlencode({
                'token' : token,
                'query_str' : query_str
            })
    r = requests.get(f"{BASE_URL}/search?{queryString}")
    return r.json()


def test_search_two_messages():
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password",
            "name_first" : "First",
            "name_last" : "Last"
        }).json()
    token = received['token'] 
    channel_id = create_channel(token)
    message_id = send_message(token, "Look its a message", channel_id)
    send_message(token, "This shouldnt be found", channel_id)   

    queryString = urllib.parse.urlencode({
                'token' : received['token'],
                'query_str' : "Look"
            })
    r = requests.get(f"{BASE_URL}/search?{queryString}")
    payload = r.json()['messages'][0]
    assert payload['message_id'] == message_id
    assert payload['message'] == 'Look its a message'   

def test_search_in_multiple_channels():
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "test@gmail.com",
            "password" : "Password",
            "name_first" : "First",
            "name_last" : "Last"
        }).json()
    print(received)
    token = received['token'] 
    # Check empty    
    print(search_messages(token, "Look"))
    channel_id = create_channel(token)
    message_id = send_message(token, "Look its a message", channel_id)
    send_message(token, "This shouldnt be found", channel_id)   
    received = requests.post(f"{BASE_URL}/auth/register", json={
            "email" : "search_test@gmail.com",
            "password" : "Password",
            "name_first" : "First",
            "name_last" : "Last"
        }).json()
    token2 = received['token']
    channel_id = create_channel(token2)
    message_id = send_message(token2, "Look anohter message", channel_id)
    send_message(token2, "This shouldnt be found either", channel_id)   
    queryString = urllib.parse.urlencode({
                'token' : received['token'],
                'query_str' : "Look"
            })
    r = requests.get(f"{BASE_URL}/search?{queryString}")
    payload = r.json()['messages']
    print(payload)
    assert len(payload) == 2
