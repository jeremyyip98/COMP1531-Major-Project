# Helper function to register a valid user and return u_id and token
def register_valid_user():
    return auth_register("test@gmail.com", "Password", "First", "Last")
