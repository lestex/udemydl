import requests

class Session:
    headers = {
        'Host': 'www.udemy.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:39.0) Gecko/20100101 Firefox/66.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.udemy.com/join/login-popup',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    def __init__(self):
        self.session = requests.sessions.Session()
        
    def set_auth_headers(self, access_token, client_id):
        self.headers['Authorization'] = 'Bearer {}'.format(access_token)

    def get(self, url):
        return self.session.get(url, headers=self.headers)

    def post(self, url, data):
        return self.session.post(url, data, headers=self.headers)

session = Session()
