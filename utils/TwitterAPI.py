import requests
import json

class TwitterAPI:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})

    def open_stream (self, **kwargs):
        url = 'https://api.twitter.com/2/tweets/search/stream'
        if kwargs:
            url += '?'
            for x in kwargs.keys():
                value = kwargs[x]
                if isinstance(value, list):
                    param = ",".join(value)
                else:
                    param = value
                url += f"{x.replace('__', '.')}={param}&"
        response = self.session.get(url, stream=True)
        iter_lines = response.iter_lines()
        def gen ():
            for x in iter_lines:
                if x:
                    yield json.loads(x)
        return gen()

    def add_rule (self, tag, value, has=[]):
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
        response = self.session.post(url, json=data)
        return True

class StreamRule:
    def __init__(self, id, value, tag):
        self.id = id
        self.value = value
        self.tag = tag

    def __str__(self):
        return f"{self.tag} ({self.value})"