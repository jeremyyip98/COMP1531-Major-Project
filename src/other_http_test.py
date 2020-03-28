import json
import urllib.request
from database import restore_channel_database, restore_database

BASE_URL = "http://127.0.0.1:10033"

def test_channels_createt_payload():
    data = json.dumps({
        'token' : 'validtoken',
        'u_id' : 1,
        'permission_id' : 1
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload['token'] == 'validtoken'
    assert payload['u_id'] == 1
    assert payload['permission_id'] == 1
    restore_channel_database()
    restore_database()