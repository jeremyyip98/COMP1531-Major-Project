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
    with open('pickle_database.p', 'wb') as FILE:
        print("Saving...")
        pickle.dump(DATA_STRUCTURE, FILE)
        
def database_update():
    '''try:
        f = open("pickle_database.p", "rb")
        f.close()
    except FileNotFoundError:
        raise InputError(description='Email not found!')'''
    
    DATA = pickle.load(open("pickle_database.p", "rb"))
    print(DATA)
    database.u_ids = DATA['u_ids']
    database.channel_ids = DATA['channel_ids']
    database.registered_users_store = DATA['registered_users_store']
    database.list_of_channels = DATA['list_of_channels']
    database.message_list = DATA['message_list']
    database.standup_queue = DATA['standup_queue']
    print("Updating...")
