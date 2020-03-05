from auth import auth_register
from channels import channels_create
from message import message_send

# Helper function to register a valid user and return u_id and token
def register_valid_user():
    return auth_register("test@gmail.com", "Password", "First", "Last")

def register_another_valid_user():
    return auth_register("anothertest@gmail.com", "Anotherpassword", "Anotherfirst", "Anotherlast")

def create_valid_channel(channel_name, is_public):
    details = register_valid_user()
    return (channels_create(details["token"], channel_name, is_public), details) 



