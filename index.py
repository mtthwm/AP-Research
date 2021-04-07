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
from utils.CommandLineArgs import CommandLineArgs
from concurrent.futures import ThreadPoolExecutor

def main (txt_file:str, sequence_length:int, search_term:str, retain_originals:bool, retain_finals:bool):
    ORIGINAL_IMG_DIR = 'images/originals/'
    FINAL_IMG_DIR = 'images/final/'

    twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))

    twitter.clear_rules()
    twitter.add_rule('Posts with images', search_term, has=['images'])

    tweet_stream = twitter.open_stream(expansions='attachments.media_keys', media__fields=['url'])

    image_paths = []

    total_bits_generated = 0
    
    start_time = time()
           
    executor = ThreadPoolExecutor()
    for x in tweet_stream:
        if total_bits_generated >= sequence_length:
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

args = CommandLineArgs(sys.argv, 'file:str:!', 'sequence_length:int:!', 'retain_originals:bool:False', 'retain_finals:bool:False', 'search_term:str:yellowstone')
print(args._arguments)
main(filename, sequence_length=args.get('sequence_length'), search_term=args.get('search_term'), retain_originals=args.get('retain_originals'), retain_finals=args.get('retain_finals'))