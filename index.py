from dotenv import load_dotenv
load_dotenv()
import os
import json
from utils.TwitterAPI import TwitterAPI

twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))
twitter.clear_rules()

twitter.add_rule('Posts with images', has=['images'])

rules = twitter.get_rules()
print(rules)
for x in rules:
    print(x)
# tweet_stream = twitter.open_stream()

# print(next(tweet_stream))