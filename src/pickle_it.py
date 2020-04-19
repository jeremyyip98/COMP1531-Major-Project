'''Pickle database to store data structures.'''
import pickle
import database

def pickle_it():
    '''Combines data structures in database and stores it in pickle_database.p as a pickle file.'''
    data_structure = {
        'u_ids' : database.u_ids,
        'channel_ids' : database.channel_ids,
        'registered_users_store' : database.registered_users_store,
        'list_of_channels' : database.list_of_channels,
        'message_list' : database.message_list,
    }
    with open('pickle_database.p', 'wb') as f:
        print("Saving...")
        pickle.dump(data_structure, f)
    f.close()

def database_update():
    '''Updates the current database with the data structure stored in pickle_database.p - performed when server first opens'''
    try:
        f = open("pickle_database.p", "rb")
        data = pickle.load(f)
        # Updating each data structure in database
        database.u_ids = data['u_ids']
        database.channel_ids = data['channel_ids']
        database.registered_users_store = data['registered_users_store']
        database.list_of_channels = data['list_of_channels']
        database.message_list = data['message_list']
        # Resetting standup
        for channel in database.list_of_channels:
            channel['is_in_standup'] = False
            channel['standup_finish_time'] = None
        print("Updating...")
        f.close()
        
    except FileNotFoundError:
        pass
