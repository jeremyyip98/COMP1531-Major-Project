"""
Iteration 2
Standup functions
Jeffrey Yang z5206134
"""
import threading
import database
from error import InputError
from message import message_send

def convert_standup_queue(s_q):
    '''converts the standup queue in database (which is a list of msg dicts)
    into a single message string'''
    compiled_mesage = ""
    if s_q:
        for msg_dict in s_q:
            compiled_mesage = compiled_mesage + msg_dict['name_first'] + ": " + msg_dict['message'] + "\n" #pylint: disable=line-too-long
    return compiled_mesage

def send_standup_queue(token, channel_id):
    ''' helper function for sending standup queue at the end of standup'''
    standup_queue = database.get_standup_queue()
    compiled_mesage = convert_standup_queue(standup_queue)
    message_send(token, channel_id, compiled_mesage)
    database.restore_standup_queue()

def standup_start(token, channel_id, length):
    '''initiates a standup in a channel'''
    database.check_token(token)
    if not database.check_channel_exists(channel_id):
        raise InputError(description='Channel id is not a valid channel id')
    database.turn_on_standup(channel_id, length)
    #turn off standup mode at the end of the timer
    standup_timer = threading.Timer(length, database.turn_off_standup, args=[channel_id])
    standup_timer.start()
    #send the standup queue message at the end of the timer
    queue_timer = threading.Timer(length, send_standup_queue, args=[token, channel_id])
    queue_timer.start()
    return {'time_finish' : database.get_standup_finish_time(channel_id)}

def standup_active(token, channel_id):
    '''checks if a channel is in a standup. Returns the time the stand up is set to finish'''
    database.check_token(token)
    if not database.check_channel_exists(channel_id):
        raise InputError(description='Channel id is not a valid channel id')
    time = database.get_standup_finish_time(channel_id)
    return {'is_active': database.check_standup_happening(channel_id), 'time_finish' : time}

def standup_send(token, channel_id, message):
    '''sends a message to be buffered in the standup queue'''
    database.check_token(token)
    if not database.check_channel_exists(channel_id):
        raise InputError(description='Channel id is not a valid channel id')
    if len(message) > 1000:
        raise InputError(description='Message is over 1000 characters')
    if not database.check_standup_happening(channel_id):
        raise InputError(description='An active standup is not corrently happening')
    person = database.get_formatted_user(token)
    name = person['name_first']
    standup_queue = database.get_standup_queue()
    standup_queue.append({
        'name_first' : name,
        'message' : message,
    })
