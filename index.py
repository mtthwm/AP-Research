from dotenv import load_dotenv
load_dotenv()
import os
import json
from utils.TwitterAPI import TwitterAPI

twitter = TwitterAPI(os.getenv('TWITTER_API_BEARER_TOKEN'))
twitter.clear_rules()

twitter.add_rule('Posts with images', has=['images'])

for x in twitter.get_rules():
    print(x) 

# for response_line in twitter.open_stream():
#     if response_line:
#         json_response = json.loads(response_line)
#         print(json.dumps(json_response, indent=4, sort_keys=True))