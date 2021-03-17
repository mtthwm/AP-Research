from dotenv import load_dotenv
load_dotenv()
import os
import json
import shutil
from utils.TwitterAPI import TwitterAPI
from PIL import Image
from utils.functions import arnold_cat_map, download_url_image
from datetime import datetime

def main (txt_file:str, num_blocks:int=1):
    ORIGINAL_IMG_DIR = 'images/originals/'
    FINAL_IMG_DIR = 'images/final/'

    twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))

    twitter.clear_rules()
    twitter.add_rule('Posts with images', 'landscape', has=['images'])

    tweet_stream = twitter.open_stream(expansions='attachments.media_keys', media__fields=['url'])

    image_paths = []

    for x in tweet_stream:
        if len(image_paths) >= num_blocks:
            break
        local_image_name = ""
        try:
            for y in x['includes']['media']:
                local_image_name = download_url_image(y['url'], ORIGINAL_IMG_DIR)
                break
            image_paths.append(arnold_cat_map(local_image_name, os.path.join(FINAL_IMG_DIR, datetime.now().strftime("%m%d%Y%M%S%f")+".png"), txt_file))
        except KeyError as e:
            print('DOES NOT CONTAIN MEDIA')

    for i in image_paths:
        print(i)

filename = os.path.join("data/", datetime.now().strftime("%m-%d-%Y[%M%S]") + ".txt")
main(filename, num_blocks=2)