"""
UNSW Comp1531 Iteration 1
Channel Test 1
Jackie Cai z5259449
"""
import pytest

from database import restore_channel_database, restore_database
from error import AccessError, InputError
from auth import auth_register
from user import user_profile
from channels import channels_create, channels_list, channels_listall
from channel import channel_addowner, channel_removeowner, channel_invite, channel_details, channel_join, channel_leave

def test_channels_create_access_error():
    """test invalid token"""
    with pytest.raises(AccessError) as err:
        channels_create('hopefullythisnotavalidtoken', 'a', True)
def test_channels_create_input_error():
    """This function test the input errors in requirements"""
    #test if there is an input error when character string is greater than 20
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    with pytest.raises(InputError) as err:
        channels_create(user1['token'], 'a' * 21, True)
def test_channels_create_return():
    restore_channel_database()
    """test that the channel create returns the right token"""
    user1 = auth_register('name1@mail.com', 'password', 'Jim', 'Smith')
    #test if it returns the right ID
    channel1 = channels_create(user1['token'], 'My Channel', True)
    channel_list = channels_listall(user1['token'])
    #should only show the channels the user token given is in
    assert channel1 == channel_list[0]['channel_id']
def test_channel_list_access_error():
    """test the token error"""
    #test invalid token
    with pytest.raises(AccessError) as err:
        channels_list('hopefullythisnotavalidtoken')
def test_channel_list_normal():
    """test that list only has one channel for both user even if the channel1 is public"""
    restore_database()
    restore_channel_database()
    user1 = auth_register('name2@mail.com', 'password', 'Jim', 'Smith')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    #create chanel_list
    channel_list = channels_list(user1['token'])
    #make sure there is only one channel
    assert channel_list[0]['channel_id'] == channel1
    assert len(channel_list) == 1
    #check info is right
    details = channel_details(user1['token'], channel1)
    assert details['name'] == channel_list[0]['channel_name']
    #test that after channel_list2 is created channel1 isn't in it
    user2 = auth_register('name3@mail.com', 'password1', 'Tim', 'Lift')
    channel2 = channels_create(user2['token'], 'Second Channel', False)
    #make second channellist to test if it only shows for user2
    channel_list2 = channels_list(user2['token'])
    #check it is in the channelList2
    assert channel_list2[0]['channel_id'] == channel2
    assert len(channel_list2) == 1
    #make sure all the details are right
    details = channel_details(user2['token'], channel2)
    assert details['name'] == channel_list2[0]['channel_name']
def test_channel_listall_access_error():
    """check if inputed invalid token gives errors"""
    with pytest.raises(AccessError) as err:
	    channels_listall('hopefullythisnotavalidtoken')
def test_channel_listall_normal():
    """channel list all should list all channels regardless if the user is in the channel or not"""
    restore_database()
    restore_channel_database()
    user1 = auth_register('name4@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name5@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    channel2 = channels_create(user2['token'], 'Second Channel', False)
    channel_list = channels_listall(user1['token'])
    #make sure it shows both channels for one user even if user is not in
    #the channel
    assert channel_list[0]['channel_id'] == channel1
    assert channel_list[1]['channel_id'] == channel2
def test_channel_addowner_access_error():
    restore_channel_database()
    """test access errors for token and authorisation"""
    #assume user1 is owner of channel when he makes the channel
    user1 = auth_register('name6@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name7@mail.com', 'password', 'Tim', 'Slim')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    #check that when inputed wrong token gives access error
    with pytest.raises(AccessError) as err:
	    channel_addowner('hopefullythisnotavalidtoken', channel1, user1['u_id'])
    #trying to add user2 as owner when the given person is not a owner 
    with pytest.raises(AccessError) as err:
        channel_addowner(user2['token'], channel1, user2['u_id'])
def test_channel_addowner_input_error():
    """test input error for other parameters"""
    user1 = auth_register('name8@mail.com', 'password', 'Jim', 'Smith')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    #test if the channel adds user1 again it gives InputError
    with pytest.raises(InputError) as err:
	    channel_addowner(user1['token'], channel1, user1['u_id'])
    #test if the channel tries to add channel_id invalid id
    with pytest.raises(InputError) as err:
	    channel_addowner(user1['token'], channel1, user1['u_id'])
def test_channel_addowner_normal():
    """test return types and the function does what it suppose to do"""
    restore_database()
    restore_channel_database()
    user1 = auth_register('name9@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name10@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)  
    #invites user2 to channel
    channel_invite(user1['token'], channel1, user2['u_id'])
    #test if the unauthorises user tries to add himself as owner
    with pytest.raises(AccessError) as err:
	    channel_addowner(user2['token'], channel1, user2['u_id'])   
    #adds user2 as owner and get details
    channel_addowner(user1['token'], channel1, user2['u_id'])
    details = channel_details(user2['token'], channel1)
    #assert that user 2 is in owners through the details function
    user2_profile = user_profile(user2['token'], user2['u_id'])
    assert details['owner_members'][1] == user2_profile['user']['u_id']
def test_channel_remove_owner_access_error():
    """"test access error for remove owner"""
    #assume user1 is owner of channel when he makes the channel
    user1 = auth_register('name11@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name12@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    #Test that when inputed invalid token access error is raised
    with pytest.raises(AccessError) as err:
	    channel_removeowner('hopefullythisnotavalidtoken', channel1, user1['u_id'])
    #test remove owner when user2 treis to remove user1
    with pytest.raises(AccessError) as err:
	    channel_removeowner(user2['token'], channel1, user1['u_id'])
def test_channel_remove_owner_input_error():
    """test input error for parameters"""
    user1 = auth_register('name13@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name14@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    #test invalid id channel
    with pytest.raises(InputError) as err:
	    channel_removeowner(user1['token'], channel1 + 10, user1['u_id'])
    #test remove owner when user2 is not owner
    with pytest.raises(InputError) as err:
	    channel_removeowner(user1['token'], channel1, user2['u_id'])
def test_channel_remove_owner_normal():
    """test function works and return type is correct"""
    restore_database()
    restore_channel_database()
    user1 = auth_register('name15@mail.com', 'password', 'Jim', 'Smith')
    user2 = auth_register('name16@mail.com', 'password1', 'Tim', 'Lift')
    channel1 = channels_create(user1['token'], 'My Channel', True)
    details = channel_details(user1['token'], channel1)
    channel_addowner(user1['token'], channel1, user2['u_id'])
    #checking that the owners are user1 and user2
    user1_profile = user_profile(user1['token'], user1['u_id'])
    assert details['owner_members'][0] == user1_profile['user']['u_id']
    user2_profile = user_profile(user2['token'], user2['u_id'])
    assert details['owner_members'][1] == user2_profile['user']['u_id']
    assert len(details['owner_members']) == 2
    channel_removeowner(user2['token'], channel1, user2['u_id'])
    #check that after removing the user2 as owner there is only one owner
    assert len(details['owner_members']) == 1
def test_channel_leave_access_error():
    """test the access error for token and other"""
    user1 = auth_register('name101@mail.com', 'password12', 'Slate', 'Sa')
    user2 = auth_register('name17@mail.com', 'password1', 'Mate', 'Smith')
    channel = channels_create(user2['token'], 'valid_channel', True)
    #Test that when inputed invalid token access error is raised
    with pytest.raises(AccessError) as err:
	    channel_leave('hopefullythisnotavalidtoken', channel)
    #test Access error when user is not memeber of channel
    with pytest.raises(AccessError) as err:
	    channel_leave(user1['token'], channel)
def test_channel_leave_input_error():
    """test the input error for the parameters"""
    user = auth_register('name18@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    #test inputerror with an invalid channel_id
    with pytest.raises(InputError) as err:
	    channel_leave(user['token'], channel + 10)
    #test inputerror with invalid channel_id again
    with pytest.raises(InputError) as err:
	    channel_leave(user['token'], channel + 1)
def test_channel_leave_normal():
    """test leave function works"""
    restore_database()
    restore_channel_database()
    user = auth_register('name19@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', True)
    details = channel_details(user['token'], channel)
    #make sure the only memeber is the person who created it
    assert len(details['all_members']) == 1
    channel_leave(user['token'], channel)
    if not details['all_members']:
	    pass
def test_channel_join_error():
    """test the input and access errors for the function parameters"""
    user = auth_register('name20@mail.com', 'password', 'John', 'Doe')
    user2 = auth_register('name21@mail.com', 'passw0rd', 'Ben', 'Ny')
    channel = channels_create(user['token'], 'valid_channel', False)
    #Test that when inputed invalid token access error is raised
    with pytest.raises(AccessError) as err:
	    channel_join('hopefullythisnotavalidtoken', channel)   
    #test input error when the channel id is invalid
    with pytest.raises(InputError) as err:
	    channel_join(user['token'], channel + 10)   
    #test access error when the channel is private and user2 is not admin
    with pytest.raises(AccessError) as err:
	    channel_join(user2['token'], channel)
def test_channel_join_normal():
    """test the function works and returns what it's suppose to"""
    restore_database()
    restore_channel_database()
    user = auth_register('name22@mail.com', 'password', 'John', 'Doe')
    user2 = auth_register('name23@mail.com', 'passw0rd', 'Ben', 'Ny')
    channel2 = channels_create(user2['token'], 'Public Channel', True)
    #test user joining a public channel
    details = channel_details(user2['token'], channel2)
    assert len(details['all_members']) == 1
    #test there are now 2 people in the channel
    channel_join(user['token'], channel2)
    assert len(details['all_members']) == 2
def test_channel_join_already_in():
    user = auth_register('name24@mail.com', 'password', 'John', 'Doe')
    channel = channels_create(user['token'], 'valid_channel', False)
    with pytest.raises(InputError) as err:
    	channel_join(user['token'], channel)

