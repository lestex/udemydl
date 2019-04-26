import requests

class Session:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'www.udemy.com',
        'Referer': 'https://www.udemy.com/join/login-popup'
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
