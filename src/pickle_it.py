"""
pickle_it.py
"""
import pickle
import database
from channels import channels_list

def pickle_it():
    """Main function for pickle"""
    DATA_STRUCTURE = {
        'u_ids' : database.u_ids,
        'channel_ids' : database.channel_ids,
        'registered_users_store' : database.registered_users_store,
        'list_of_channels' : database.list_of_channels,
        'message_list' : database.message_list,
    }
    with open('pickle_database.p', 'wb') as FILE:
        print("Saving...")
        pickle.dump(DATA_STRUCTURE, FILE)
    FILE.close()

def database_update():
    try:
        FILE = open("pickle_database.p", "rb")
        DATA = pickle.load(FILE)
        # Updating each data structure in database
        database.u_ids = DATA['u_ids']
        database.channel_ids = DATA['channel_ids']
        database.registered_users_store = DATA['registered_users_store']
        database.list_of_channels = DATA['list_of_channels']
        database.message_list = DATA['message_list']
        # Resetting standup
        for channel in database.list_of_channels:
            channel['is_in_standup'] = False
            channel['standup_finish_time'] = None
        print("Updating...")
        FILE.close()
        
    except FileNotFoundError:
        pass
    
    

