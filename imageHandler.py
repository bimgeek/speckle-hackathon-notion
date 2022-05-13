from imgurpython import ImgurClient
import base64

def uploadImage(img_path):
    client = ImgurClient(client_id='f4975762ca0337e', client_secret='30a10abd8900e58fcbf8cc7137aecf1bd3607ae7')
    image = client.upload_from_path(img_path)
    return image

def downloadImage(img_string, img_name):
    img_split = img_string.split(',')
    sc_base64 = img_split[1]
    img_path = "comment_images\{}.png".format(img_name)

    with open(img_path, "wb") as fh:
        fh.write(base64.b64decode(sc_base64))
    
    return img_path
