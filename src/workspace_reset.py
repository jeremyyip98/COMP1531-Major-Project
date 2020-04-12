import database

def workspace_reset():
    database.restore_channel_database()
    database.restore_database()
    database.restore_standup_queue()
    database.reset_message()
