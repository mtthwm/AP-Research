from dotenv import load_dotenv
load_dotenv()
import os
import json
import shutil
from utils.TwitterAPI import TwitterAPI
from PIL import Image
from utils.functions import arnold_cat_map, download_url_image
from datetime import datetime
import sys

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
        try:
            y = x['includes']['media'][0]
            url = y['url']
            filename = os.path.join(ORIGINAL_IMG_DIR, url.split('/')[-1])
            if os.path.exists(filename):
                print("Image has been downloaded previously.")                
            else:
                local_image_name = download_url_image(url, filename)
                image_paths.append(arnold_cat_map(local_image_name, os.path.join(FINAL_IMG_DIR, datetime.now().strftime("%m%d%Y%H%M%S%f")+".png"), txt_file))
                local_image_name = ""
        except KeyError as e:
            print('DOES NOT CONTAIN MEDIA')
            pass

    for i in image_paths:
        print(i)

filename = os.path.join("data/", datetime.now().strftime("%m-%d-%Y(%H%M%S)") + ".txt")
try:
    main(filename, num_blocks=int(sys.argv[1]))
except IndexError:
    raise Exception("Please include block number.")
except ValueError:
    raise Exception("Invalid value for block number.")