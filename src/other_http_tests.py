'''
Test for Other functions like search and admin
'''
#pylint: disable=C0103, W0601, C0303
import json
import urllib
import requests
import urllib.request

PORT = 8084
BASE_URL = f"http://127.0.0.1:{PORT}"

# Helper Functions 
def register_admin():
    '''Helper function to make an admin'''
    admin = requests.post(f"{BASE_URL}/admin/create", json={})
    return admin.json()

def register_example_user():
    '''Helper function that adds a user to database'''
    received = requests.post(f"{BASE_URL}/auth/register", json={
        "email" : "othertest@gmail.com",
        "password" : "Password",
        "name_first" : "Other",
        "name_last" : "Last"
        })
    return received.json()

def get_user_all(token):
    '''Helper function that gets all info on a user'''
    queryString = urllib.parse.urlencode({'token' : token})
    r = requests.get(f"{BASE_URL}/users/all?{queryString}")
    return r.json()

def channel_details_get(token, channel_id):
    '''Helper function to get channel details to check in server'''
    queryString = urllib.parse.urlencode({
        'token' : token,
        'channel_id' : channel_id,
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{queryString}")
    payload = json.load(response)
    return payload

def channel_details_get2(token, channel_id):
    '''Helper function to get channel details to check in server 2'''
    queryString = urllib.parse.urlencode({
        'token' : token,
        'channel_id' : channel_id,
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{queryString}")
    payload = response.json()
    return payload

def create_channel(token):
    '''Helper function to create a channel'''
    payload = requests.post(f"{BASE_URL}/channels/create", json={
        'token' : token,
        'channel_name' : 'test_channel',
        'is_public' : True,
    })
    return payload.json()['channel_id']

def create_channel2(token):
    '''Helper function to create another channel'''
    requests.post(f"{BASE_URL}/channels/create", json={
        'token' : token,
        'channel_name' : 'test_channel',
        'is_public' : True,
    })
    
def send_message(token, message, channel_id):
    '''Helper function sending message to test search'''
    message_id = requests.post(f"{BASE_URL}/message/send", json={
        "token" : token,
        "channel_id" : channel_id,
        "message" : message
        }).json() 
    return message_id['message_id']

def search_messages(token, query_str):
    '''helper function to search for message'''
    queryString = urllib.parse.urlencode({
                'token' : token,
                'query_str' : query_str
    })
    r = requests.get(f"{BASE_URL}/search?{queryString}")
    return r.json()
# test Functions
def test_users_all():
    '''Test user all'''
    requests.post(f"{BASE_URL}/workspace/reset", json={}) 
    details = register_example_user()
    queryString = urllib.parse.urlencode({'token' : details['token']})
    r = requests.get(f"{BASE_URL}/users/all?{queryString}")
    response = r.json()['users'][0]
    assert response['email'] == 'othertest@gmail.com'
    assert response['name_first'] == 'Other'

def test_users_all_more():
    '''More user all test'''
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

def test_search_two_messages():
    '''Search for two message to test search'''
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
    '''test the search multi channel'''
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

def test_admin_permission_change():
    '''Test the permission change for user http'''
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    user = register_example_user()
    admin = register_admin()
    details = get_user_all(user['token'])
    assert details['users'][0]['permission_id'] == 2
    requests.post(f"{BASE_URL}/admin/userpermission/change", json={
        "token" : admin['token'],
        "u_id" : user['u_id'],
        "permission_id" : 1
    })
    details = get_user_all(user['token'])
    assert details['users'][0]['permission_id'] == 1
    requests.post(f"{BASE_URL}/admin/userpermission/change", json={
        "token" : admin['token'],
        "u_id" : user['u_id'],
        "permission_id" : 2
    })
    details = get_user_all(user['token'])
    assert details['users'][0]['permission_id'] == 2

def test_admin_user_remove():
    '''Test the user remove http'''
    requests.post(f"{BASE_URL}/workspace/reset", json={})
    user = register_example_user()
    admin = register_admin()
    create_channel2(user['token'])
    c_details = channel_details_get2(user['token'], 1)
    u_details = get_user_all(user['token'])
    #make sure there are two users user and admin
    assert len(u_details['users']) == 2
    # Make sure the channel is made properly and users in channel
    owner_list = [{
        'u_id': user['u_id'],
        'name_first': 'Other',
        'name_last': 'Last'
    }]
    member_list = [{
        'u_id': user['u_id'],
        'name_first': 'Other',
        'name_last': 'Last'
    }]
    assert c_details == {
        'name' : 'test_channel',
        'owner_members' : owner_list,
        'all_members' : member_list
    }
    requests.post(f"{BASE_URL}/channel/join", json={
        'token' : admin['token'],
        'channel_id' : 1
    })
    requests.delete(f"{BASE_URL}/admin/user/remove", json={
        'token' : admin['token'],
        'u_id' : user['u_id']
    })
    u_detail = get_user_all(admin['token'])
    # one user which is admin
    assert len(u_detail['users']) == 1
    assert u_detail['users'][0]['name_first'] == 'Admin'
    c_detail = channel_details_get2(admin['token'], 1)
    owner_list = [{
        'u_id': admin['u_id'],
        'name_first': 'Admin',
        'name_last': 'Nimda'
    }]
    member_list = [{
        'u_id': admin['u_id'],
        'name_first': 'Other',
        'name_last': 'Nimda'
    }]
    assert c_detail == {
        'name' : 'test_channel',
        'owner_members' : owner_list,
        'all_members' : member_list
    }
