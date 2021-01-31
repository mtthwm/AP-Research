import requests
from .Classes import StreamRule

class TwitterAPI:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})

    def open_stream (self):
        url = 'https://api.twitter.com/2/tweets/search/stream'
        response = self.session.get(url, stream=True)
        return response.iter_lines()

    def add_rule (self, tag, value='', has=[]):
        url = 'https://api.twitter.com/2/tweets/search/stream/rules'
        data = {
            'add': [
                {'value': f'{value} ', 'tag': tag}
            ]
        }
        for x in has:
            data['add'][0]['value'] += f'has:{x}'
        response = self.session.post(url, json=data)
        return response

    def get_rules (self):
        url = 'https://api.twitter.com/2/tweets/search/stream/rules'
        response = self.session.get(url)
        rules = []
        json = response.json()
        for x in json.get('data', []):
            rules.append(StreamRule(x['id'], x['value'], x['tag']))
        return rules

    def clear_rules (self):
        url = 'https://api.twitter.com/2/tweets/search/stream/rules'
        rules = self.get_rules()
        rule_ids = list(map(lambda x : str(x.id), rules))
        data = {
            'delete': {
                'ids': rule_ids
            }
        }
        print(data)
        response = self.session.post(url, json=data)
        print(response.json())
        return True

