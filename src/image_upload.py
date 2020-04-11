import requests
import uuid
import database
from error import AccessError, InputError
from PIL import Image
from secrets import urlsa


def upload_profile_pic(token, img_url, x_start, y_start, x_end, y_end):
    database.check_token(token)
    # Get Image    
    """ Downloads the image from url and saves it at filename """
    r = requests.get(img_url, allow_redirects=True)
    if r.status_code != 200:
        raise InputError(description='Image could not be accessed')    
    filename = f"profile_pictures/{uuid.uuid4().hex}"
    # Should Check folder is there first
    
    open(filename, 'wb').write(r.content)
    """ Opens the image using pillow """
    im = Image.open('image')
    if im.format != 'jpeg':
        raise InputError(description='Image is not a .jpg')
    coordinates = (x_start, y_start, x_end, y_end)
    width, height = im.size
    if x_start > width or x_end > width or y_start > height or y_end > height:
        raise InputError(description='Crop out of bounds')
    for c in coordinates:
        if c < 0:
            raise InputError(description='Crop out of bounds')
    """ Crops the image according to input coordinates """
    new = im.crop(coordinates)    
    new.save(filename, format='jpg')
    # Then needs to host url and link the profile picture to user structure

