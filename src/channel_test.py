from error import AccessError, InputError
from auth import auth_register
from channels import channels_create

def test_channel_create():
    user1 = auth_register('name@mail.com', 'password', 'Jim', 'Smith')
    with pytest.raises(InputError) as e:
        channels_create(user1['token'], 'a' * 21, True)
        
    