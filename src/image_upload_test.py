import pytest
from image_upload import upload_profile_pic
from helper_functions import register_valid_user

def test_upload_profile_pic():
    token = register_valid_user()['token']
    img_url = "https://picsum.photos/200/300.jpg"
    upload_profile_pic(token, img_url, 0, 0, 60, 60)
