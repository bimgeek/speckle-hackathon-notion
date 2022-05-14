from imgurpython import ImgurClient
import base64
import os

def uploadImage(img_path):
    # Upload image to imgur
    client = ImgurClient(client_id='f4975762ca0337e', client_secret='30a10abd8900e58fcbf8cc7137aecf1bd3607ae7')
    image = client.upload_from_path(img_path)

    # delete file on disk
    if os.path.exists(img_path):
        os.remove(img_path)

    return image

def downloadImage(img_string, img_name):
    # Get base64 encode from screenshot string
    img_split = img_string.split(',')
    sc_base64 = img_split[1]

    # Image save path
    img_path = "comment_images\{}.png".format(img_name)

    # Write image to disk
    with open(img_path, "wb") as fh:
        fh.write(base64.b64decode(sc_base64))
    
    return img_path
