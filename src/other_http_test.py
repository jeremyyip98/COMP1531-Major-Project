import requests
from database import registered_users_store
from channel_http_test import create_user1, create_user2

BASE_URL = "http://127.0.0.1:10013"

def test_channels_createt_payload():
    user1 = create_user1()
    user2 = create_user2()
    requests.post(f"{BASE_URL}/admin/userpermission/change", json={
        'token' : user1['token'],
        'u_id' : user2['u_id'],
        'permission_id' : 1,
    })
    for i in registered_users_store['registered_users']:
        if user2['u_id'] == i['u_id']:
            assert i['permission_id'] == 1
