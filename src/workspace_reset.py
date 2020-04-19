'''
COMP1531
Workspace reset
'''
import database

def workspace_reset():
    '''
    Resets the database
    '''
    database.restore_channel_database()
    database.restore_database()
    database.restore_standup_queue()
    database.reset_message()
