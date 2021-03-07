from dotenv import load_dotenv
load_dotenv()
import os
import json
from utils.TwitterAPI import TwitterAPI
from utils.functions import download_url_image

twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))

twitter.clear_rules()
twitter.add_rule('Posts with images', 'landscape', has=['images'])

tweet_stream = twitter.open_stream(expansions='attachments.media_keys', media__fields=['url'])

tweet = next(tweet_stream)
print(tweet, type(tweet))

for x in tweet['includes']['media']:
    download_url_image(x['url'], directory='/images/originals')
