from . import __title__
import time
import logging

logger = logging.getLogger(__title__)

class UdemyDownload(object):
    def __init__(self, course_url, username, password, output_dir):

        self.username = username
        self.password = password
        self.course_url = course_url
        self.output_dir = output_dir
    
    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *args):
        self.logout()
    
    def login(self):
        logger.info('Logging in ...')
        time.sleep(1)

    def logout(self):
        logger.info('Logged Out!')
        time.sleep(1)

    def analyze(self):
        logger.info('Analyzing ...')
        time.sleep(5)

    def download(self):
        logger.info('Downloading files ...')
        time.sleep(5)
        logger.info('Downloaded all files.')
