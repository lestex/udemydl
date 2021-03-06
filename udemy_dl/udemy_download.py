from .session import session
from .exceptions import UdemyException
from .course import Course
from .downloader import Downloader
from .utils import LOGIN_URL, LOGOUT_URL
from . import logger
import re
import cloudscraper


class UdemyDownload(object):
    def __init__(self, course_url, username, password, output_dir, quality):
        self.username = username
        self.password = password
        self.course_url = course_url
        self.output_dir = output_dir
        self.quality = quality
        self.session = session
        self.data_links = None
        self._scraper = cloudscraper.create_scraper()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *args):
        self.logout()

    def _get_csrf_token(self):
        response = self._scraper.get(LOGIN_URL)
        match = re.search('name=\"csrfmiddlewaretoken\" value=\"(.*)\"', response.text)
        return match.group(1)

    def login(self):
        logger.info('Trying to log in ...')
        csrf_token = self._get_csrf_token()
        payload = {
            'email': self.username,
            'password': self.password,
            'csrfmiddlewaretoken': csrf_token,
            'locale': 'en_US',
            'submit': 'Log In'
        }
        self._scraper.headers.update({"Referer": LOGIN_URL})
        response = self._scraper.post(LOGIN_URL, data=payload, allow_redirects=False)

        access_token = response.cookies.get('access_token')
        client_id = response.cookies.get('client_id')

        response_text = response.text

        if 'check your email and password' in response_text:
            raise UdemyException('Wrong Username or Password!')

        elif access_token is None:
            raise UdemyException('Couldn\'t fetch token!')

        elif 'error' in response_text:
            raise UdemyException('Found error in login page')

        self.session.set_auth_headers(access_token, client_id)
        logger.info("Login success.")

    def logout(self):
        self.session.get(LOGOUT_URL)
        logger.info('Logged Out!')

    def analyze(self):
        logger.info('Analyzing the course ...')
        course = Course(self.course_url, self.session)
        self.data_links = course.get_course_data(self.quality)
        logger.debug('data links: %s', self.data_links)

    def download(self):
        logger.info('Downloading files ...')
        Downloader(self.data_links, self.output_dir).download()
        logger.info('Downloaded all files.')
