from database import check_token, get_all_users

# Probably should need permission to do this!!!

def users_all(token):
    check_token(token)
    return {'users' : get_all_users()}

def search():
    pass
    
def standup_start():
    pass