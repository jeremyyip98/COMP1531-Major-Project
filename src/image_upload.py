import requests
import os
import uuid
import database
from error import AccessError, InputError
from PIL import Image

DIRECTORY = "profile_pictures"

def upload_profile_pic(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Function that enables the uploading of profile pictures.
    Downloads image at img_url, crops according to coordinates and uploads to 
    the profile img url store of the user the token belongs to. 

    Parameters:
        token (str): authenticaton token of the user whose profile will change
        img_url (str): url pointing to new profile picture 
        x_start, y_start, x_end, y_end (integers): Coordinates based on the image's 
            top left corner (0,0) coordinate which must make up a box where the 
            image will be cropped
    Returns:
    '''
    database.check_token(token)
    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)  
    # Get Image    
    """ Downloads the image from url and saves it at filename """
    r = requests.get(img_url, allow_redirects=True)
    if r.status_code != 200:
        raise InputError(description='Image could not be accessed')    
    filename = f"{uuid.uuid4().hex}.jpg"
    path = f"{DIRECTORY}/{filename}"
    # Should this check for folder
    open(path, 'wb').write(r.content)
    """ Opens the image using pillow """
    im = Image.open(f"{path}")
    if im.format != 'JPEG':
        raise InputError(description='Image is not a .jpg')
    coordinates = x_start, y_start, x_end, y_end
    width, height = im.size
    if x_start > width or x_end > width or y_start > height or y_end > height:
        raise InputError(description='Crop out of bounds')
    for c in coordinates:
        if c < 0:
            raise InputError(description='Crop out of bounds')
    """ Crops the image according to input coordinates """
    new = im.crop(coordinates)    
    new.save(path, format='jpeg')   
    database.set_img_url (token, f"/imgurl/{filename}")
   
    print(path)

