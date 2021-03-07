import requests
import shutil

def download_url_image (url, filename=None, directory=''):
    if not filename:
        filename = directory+url.split('/')[-1]
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    with open(filename, 'w') as file:
        shutil.copyfileobj(r.raw, file)

# def arnold_cat ():
