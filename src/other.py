from database import check_token, get_all_users

# Probably should need permission to do this!!!

def users_all(token):
    check_token(token)
    return {get_all_users()}

def search(token, query_str):
    check_token(token)
    query_str_matches = []
    messages = get_message()
    for message in messages:
        if query_str in message['message']:
            query_str_matches.append(message)
    query_str_matches =  sorted(query_str_matches, key = lambda i: i['time_created'], reverse=True)
    return query_str_matches

def standup_start():
    pass