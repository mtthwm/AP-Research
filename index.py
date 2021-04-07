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
from utils.Database import Database

db = Database(os.getenv('LOG_DB_NAME'))

txt_file = os.path.join("data/", datetime.now().strftime("%m-%d-%Y(%H%M%S)") + ".txt")

args = CommandLineArgs(sys.argv, 'file:str:!', 'sequence_length:int:!', 'retain_originals:bool:False', 'retain_finals:bool:False', 'hashtag:str:photography')
print(args._arguments)
sequence_length = args.get('sequence_length') 
hashtag = args.get('hashtag')
retain_originals = args.get('retain_originals')
retain_finals = args.get('retain_finals')

ORIGINAL_IMG_DIR = 'images/originals/'
FINAL_IMG_DIR = 'images/final/'

twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))

twitter.clear_rules()
twitter.add_rule('Posts with images', f'#{hashtag}', has=['images'])

tweet_stream = twitter.open_stream(expansions='attachments.media_keys', media__fields=['url'])

image_paths = []

total_bits_generated = 0

sequence_id = db.start_sequence(datetime.now())
start_time = time()
        
executor = ThreadPoolExecutor()

terminate_loop = False

for x in tweet_stream:
    if terminate_loop:
        break
    try:
        for y in x['includes']['media']:
            url = y['url']
            remote_filename = url.split('/')[-1]
            image_id = remote_filename.split('.')[0]
            filename = os.path.join(ORIGINAL_IMG_DIR, remote_filename)
            if os.path.exists(filename):
                print("Image has been downloaded previously.")                
            else:
                local_image_name = download_url_image(url, filename)
                outname =  datetime.now().strftime("%m%d%Y%H%M%S%f")+f"({image_id}).png"
                seq = arnold_cat_map(filename=local_image_name, outname=os.path.join(FINAL_IMG_DIR, outname), retain_final=retain_finals, image_key=image_id, sequence_id=sequence_id, append_to_text_file=txt_file)
                db.create_image(seq)
                total_bits_generated = total_bits_generated + len(seq)
                image_paths.append(seq.outname)
                if not retain_originals:
                    os.remove(local_image_name)
            if total_bits_generated >= sequence_length:
                terminate_loop = True
                break
    except KeyError as e:
        print('DOES NOT CONTAIN MEDIA')
        pass

time_elapsed = time() - start_time
bit_rate = total_bits_generated / time_elapsed
db.end_sequence(sequence_id, total_bits_generated, time_elapsed, bit_rate, datetime.now())
print("\nGenerated: ")
for i in image_paths:
    print(i)
print(f"({total_bits_generated} bits) in {time_elapsed} sec. {total_bits_generated / time_elapsed} bits/sec")