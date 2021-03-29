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
from time import time

def main (txt_file:str, num_blocks:int=1):
    ORIGINAL_IMG_DIR = 'images/originals/'
    FINAL_IMG_DIR = 'images/final/'

    twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))

    twitter.clear_rules()
    twitter.add_rule('Posts with images', 'nature', has=['images'])

    tweet_stream = twitter.open_stream(expansions='attachments.media_keys', media__fields=['url'])

    image_paths = []

    total_bits_generated = 0
    
    start_time = time()

    for x in tweet_stream:
        if len(image_paths) >= num_blocks:
            break
        try:
            y = x['includes']['media'][0]
            url = y['url']
            remote_filename = url.split('/')[-1]
            image_id = remote_filename.split('.')[0]
            filename = os.path.join(ORIGINAL_IMG_DIR, remote_filename)
            if os.path.exists(filename):
                print("Image has been downloaded previously.")                
            else:
                local_image_name = download_url_image(url, filename)
                total_bits_generated
                seq = arnold_cat_map(local_image_name, os.path.join(FINAL_IMG_DIR, datetime.now().strftime("%m%d%Y%H%M%S%f")+f"({image_id}).png"), txt_file)
                total_bits_generated = total_bits_generated + len(seq)
                image_paths.append(seq.outname)
                local_image_name = ""
        except KeyError as e:
            print('DOES NOT CONTAIN MEDIA')
            pass

    time_elapsed = time() - start_time
    print("\nGenerated: ")
    for i in image_paths:
        print(i)
    print(f"({total_bits_generated} bits) in {time_elapsed} ms. {total_bits_generated / (time_elapsed / 1000)} bits/sec")

filename = os.path.join("data/", datetime.now().strftime("%m-%d-%Y(%H%M%S)") + ".txt")
try:
    main(filename, num_blocks=int(sys.argv[1]))
except IndexError:
    raise Exception("Please include block number.")
except ValueError:
    raise Exception("Invalid value for block number.")