import pickle
import database

def pickle_it():
    DATA_STRUCTURE = {
        'u_ids' : database.u_ids,
        'channel_ids' : database.channel_ids,
        'registered_users_store' : database.registered_users_store,
        'list_of_channels' : database.list_of_channels,
        'message_list' : database.message_list,
        'standup_queue' : database.standup_queue
    }
    print(DATA_STRUCTURE)
    print(f"new list_of_channels = {database.list_of_channels}")
    print(f"new u_id = {database.u_ids}")
    with open('pickle_database.p', 'wb') as FILE:
        print("Saving...")
        pickle.dump(DATA_STRUCTURE, FILE)
    FILE.close()
        
def database_update():
    try:
        FILE = open("pickle_database.p", "rb")
        DATA = pickle.load(FILE)
        print(DATA)
        print(f"list_of_channels = {database.list_of_channels}")
        database.u_ids = DATA['u_ids']
        database.channel_ids = DATA['channel_ids']
        database.registered_users_store = DATA['registered_users_store']
        database.list_of_channels = DATA['list_of_channels']
        print(f"new list_of_channels = {database.list_of_channels}")
        database.message_list = DATA['message_list']
        database.standup_queue = DATA['standup_queue']
        print("Updating...")
        FILE.close()
        
    except FileNotFoundError:
        pass
    
    
