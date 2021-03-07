from dotenv import load_dotenv
load_dotenv()
import os
import json
from utils.TwitterAPI import TwitterAPI
from PIL import Image
from utils.functions import arnold_cat_map, download_url_image

# twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))

# twitter.clear_rules()
# twitter.add_rule('Posts with images', 'landscape', has=['images'])

# tweet_stream = twitter.open_stream(expansions='attachments.media_keys', media__fields=['url'])
# print(next(tweet_stream))

arnold_cat_map('images/originals/doggo.jpg', 'images/final/doggo.jpg')