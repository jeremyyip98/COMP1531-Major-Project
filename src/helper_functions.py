from auth import auth_register
#from channels import channels_create
#from message import message_send

# Helper function to register a valid user and return u_id and token
def register_valid_user():
    return auth_register("test@gmail.com", "Password", "First", "Last")

# Helper function to register another valid user and return u_id and token
# This is used to test input errors where a particular value (e.g. email) is already being used by another user
def register_another_valid_user():
    return auth_register("anothertest@gmail.com", "Anotherpassword", "Anotherfirst", "Anotherlast")


# Registers a choice of two different users, creates a channel and returns details
def create_valid_channel(channel_name, different_user):
    if different_user == False:
        details = register_valid_user()
    elif different_user == True:
        details = register_another_valid_user()
    return channels_create(details["token"], channel_name, True), details