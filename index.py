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

def main (txt_file:str, num_blocks:int, search_term:str, retain_originals:bool, retain_finals:bool):
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
                outname =  datetime.now().strftime("%m%d%Y%H%M%S%f")+f"({image_id}).png"
                seq = arnold_cat_map(local_image_name, os.path.join(FINAL_IMG_DIR, outname), retain_finals, txt_file)
                total_bits_generated = total_bits_generated + len(seq)
                image_paths.append(seq.outname)
                if not retain_originals:
                    os.remove(local_image_name)
        except KeyError as e:
            print('DOES NOT CONTAIN MEDIA')
            pass

    time_elapsed = time() - start_time
    print("\nGenerated: ")
    for i in image_paths:
        print(i)
    print(f"({total_bits_generated} bits) in {time_elapsed} sec. {total_bits_generated / time_elapsed} bits/sec")

filename = os.path.join("data/", datetime.now().strftime("%m-%d-%Y(%H%M%S)") + ".txt")
try:
    search_term = "nature"
    retain_originals = False
    retain_finals = False
    try:
        search_term = sys.argv[2]
        retain_originals = sys.argv[3].lower() == "true"
        retain_finals = sys.argv[4].lower() == "true"
    except:
        pass

    main(filename, num_blocks=int(sys.argv[1]), search_term=search_term, retain_originals=retain_originals, retain_finals=retain_finals)
except IndexError:
    raise Exception("Please include block number.")
except ValueError:
    raise Exception("Invalid value for block number.")