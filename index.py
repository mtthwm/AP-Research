from dotenv import load_dotenv
load_dotenv()
import os
import json
import shutil
from utils.TwitterAPI import TwitterAPI
from PIL import Image
from utils.functions import arnold_cat_map, download_url_image
from datetime import datetime

ORIGINAL_IMG_DIR = 'images/originals/'
FINAL_IMG_DIR = 'images/final/'

twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))

twitter.clear_rules()
twitter.add_rule('Posts with images', 'landscape', has=['images'])

tweet_stream = twitter.open_stream(expansions='attachments.media_keys', media__fields=['url'])

for x in tweet_stream:
    local_image_name = ""
    try:
        for y in x['includes']['media']:
            local_image_name = download_url_image(y['url'], ORIGINAL_IMG_DIR)
            break
        arnold_cat_map(local_image_name, os.path.join(FINAL_IMG_DIR, datetime.now().strftime("%m%d%Y%M%S%f")+".png"))
    except KeyError as e:
        print('DOES NOT CONTAIN MEDIA')