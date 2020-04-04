"""
Iteration 2 
Standup.py test functions
"""
import pytest
from error import AccessError, InputError
from helper_functions import register_valid_user, register_another_valid_user
from channels import channels_create
from standup import standup_active, standup_send, standup_start, convert_standup_queue
from workspace_reset import workspace_reset
from datetime import datetime, timezone
from database import get_standup_queue
def test_standup_start_error():
    """Test the input error and access error"""
    # make user
    user1 = register_valid_user()
    channel = channels_create(user1['token'], 'Channel', True)['channel_id']
    #test invalid token
    with pytest.raises(AccessError) as err:
        standup_start('hopefullyinvalidtoken', 1, 10)
    # test invalid channel id
    with pytest.raises(InputError) as err:
        standup_start(user1['token'], 100, 10)
    #start standup
    standup_start(user1['token'], channel, 10)
    #test starting another standup
    with pytest.raises(InputError) as err:
        standup_start(user1['token'], channel, 10)
    workspace_reset()

def test_standup_start_normal():
    user1 = register_valid_user()
    channel = channels_create(user1['token'], 'Channel', True)['channel_id']
    result = standup_start(user1['token'], channel, 10)
    current_dt = datetime.now()
    #get date time and then round to 2 dp or it'll be false since from the program running
    #to the next line is a few milli second and makes it wrong
    assert round(result['time_finish'], 2) == round(current_dt.replace(tzinfo=timezone.utc).timestamp() + 10, 2)
    workspace_reset()

def test_standup_active_error():
    # make user
    user1 = register_valid_user()
    channel = channels_create(user1['token'], 'Channel', True)['channel_id']
    #test invalid token
    with pytest.raises(AccessError) as err:
        standup_active('hopefullyinvalidtoken', channel)
        # test invalid channel id
    with pytest.raises(InputError) as err:
        standup_active(user1['token'], 100)
    workspace_reset()

def test_standup_active_normal():
    # make users
    user1 = register_valid_user()
    channel = channels_create(user1['token'], 'Channel', True)['channel_id']
    # check active standup when not active
    non_active = standup_active(user1['token'], channel)
    assert non_active['is_active'] is False
    assert non_active['time_finish'] is None
    #start standup
    standup_start(user1['token'], channel, 10)
    active = standup_active(user1['token'], channel)
    #get time 
    current_dt = datetime.now()
    #check is active
    assert active['is_active'] is True
    #check time_finish returns the correct result by 2dp since time start to end is too accurate and need to
    #round it down or the milli second the program start running will ruin it
    assert round(active['time_finish'], 2) == round(current_dt.replace(tzinfo=timezone.utc).timestamp() + 10, 2)
    workspace_reset()

def test_standup_send_error():
    user1 = register_valid_user()
    user2 = register_another_valid_user()
    channel = channels_create(user1['token'], 'Channel', True)['channel_id']
    #test non active standup
    with pytest.raises(InputError) as err:
        standup_send(user1['token'], channel, 'Hello')
    #start standup
    standup_start(user1['token'], channel, 10)
    #test invalid token
    with pytest.raises(AccessError) as err:
        standup_send('hopefullyinvalidtoken', channel, 'Hello')
    #test invalid user
    with pytest.raises(AccessError) as err:
        standup_send(user2['token'], channel, 'Hello')
    #test invalid channel
    with pytest.raises(InputError) as err:
        standup_send(user1['token'], 100, 'Hello')
    #test too long
    with pytest.raises(InputError) as err:
        standup_send(user1['token'], channel, 'a' * 1001)
    workspace_reset()

def test_standup_send_normal():
    user1 = register_valid_user()
    channel = channels_create(user1['token'], 'Channel', True)['channel_id']
    standup_start(user1['token'], channel, 10)
    standup_send(user1['token'], channel, 'Hello')
    result = get_standup_queue()
    assert convert_standup_queue(result) == "First: Hello\n"
