from dotenv import load_dotenv
load_dotenv()
import os
import json
from utils.TwitterAPI import TwitterAPI

twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))

for response_line in twitter.open_stream():
    if response_line:
        json_response = json.loads(response_line)
        print(json.dumps(json_response, indent=4, sort_keys=True))