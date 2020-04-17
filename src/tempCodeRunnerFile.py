requests.post(f"{BASE_URL}/workspace/reset", json={})
    user = register_example_user()
    admin = register_admin()
    channel = create_channel(user['token'])
    u_details = get_user_all(user['token'])
    #make sure there are two users user and admin
    assert len(u_details) == 2
    c_details = channel_details_get(user['token'], channel)
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
    requests.delete(f"{BASE_URL}/admin/user/remove", json={
        'token' : admin['token'],
        'u_id' : user['u_id']
    })
    requests.post(f"{BASE_URL}/channel/join", json={
        'token' : admin['token'],
        'channel_id' : channel['channel_id']
    })
    u_details = get_user_all(user['token'])
    # one user which is admin
    assert len(u_details) == 1
    assert u_details['users'][0]['first_name'] == 'Admin'
    c_details = channel_details_get(admin['token'], channel)
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
    assert c_details == {
        'name' : 'test_channel',
        'owner_members' : owner_list,
        'all_members' : member_list
    }
