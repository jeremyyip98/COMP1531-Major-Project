from error import InputError
import database
import threading
import helper_functions
from error import InputError, AccessError
from message import message_send


def send_standup_queue(token, channel_id):
    ''' helper function for sending standup queue at the end of standup'''
    standup_queue = database.get_standup_queue()
    message_send(token, channel_id, standup_queue)
    standup_queue = ""

def standup_start(token, channel_id, length):
    database.check_token(token)
    if not database.check_channel_exists(channel_id):
        raise InputError(description='Channel id is not a valid channel id')
    database.turn_on_standup(channel_id, length)
    standup_timer = threading.Timer(length, database.turn_off_standup, args=[channel_id])
    standup_timer.start()
    queue_timer = threading.Timer(length, send_standup_queue, args=[token, channel_id])
    queue_timer.start()
    return {'time_finish' : database.get_standup_finish_time(channel_id)}

def standup_active(token, channel_id):
    database.check_token(token)
    if not database.check_channel_exists(channel_id):
        raise InputError(description='Channel id is not a valid channel id')
    time = database.get_standup_finish_time(channel_id)
    return {'is_active': database.check_standup_happening(channel_id), 'time_finish' : time}

def standup_send(token, channel_id, message):
    database.check_token(token)
    if not database.check_channel_exists(channel_id):
        raise InputError(description='Channel id is not a valid channel id')
    if len(message) > 1000:
        raise InputError(description='Message is over 1000 characters')
    if not database.check_standup_happening(channel_id):
        raise InputError(description='An active standup is not corrently happening')
    if not database.check_user_in_channel(token, channel_id):
        raise AccessError(description='The authorised user is not a member of channel')
    person = database.get_formatted_user(token)
    name = person['name_first']
    standup_queue = database.get_standup_queue()
    standup_queue = standup_queue + " " + name + ": " + message + "\n"
    # What if standup_queue is longer than 1000 characters?
