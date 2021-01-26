import requests

class TwitterAPI:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def open_stream (self):
        url = 'https://api.twitter.com/2/tweets/search/stream'
        response = self.session.get(url, stream=True)
        return response.iter_lines()