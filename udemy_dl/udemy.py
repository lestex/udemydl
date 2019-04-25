from . import __title__
from .session import session
from .exceptions import UdemyException
import time
import logging
import re
import sys
import json

logger = logging.getLogger(__title__)

LOGIN_URL = 'https://www.udemy.com/join/login-popup/?displayType=ajax&display_type=popup&showSkipButton=1&returnUrlAfterLogin=https%3A%2F%2Fwww.udemy.com%2F&next=https%3A%2F%2Fwww.udemy.com%2F&locale=en_US'
LOGIN_POPUP_URL = 'https://www.udemy.com/join/login-popup'
COURSE_TITLE_URL = 'https://www.udemy.com/api-2.0/courses/{course_id}?fields[course]=title'
COURSE_INFO_URL = 'https://www.udemy.com/api-2.0/courses/{course_id}/cached-subscriber-curriculum-items?fields[asset]=@min,title,filename,asset_type,external_url,length&fields[chapter]=@min,description,object_index,title,sort_order&fields[lecture]=@min,object_index,asset,supplementary_assets,sort_order,is_published,is_free&fields[quiz]=@min,object_index,title,sort_order,is_published&page_size=550'

class UdemyDownload(object):
    def __init__(self, course_url, username, password, output_dir, session=session):
        self.username = username
        self.password = password
        self.course_url = course_url
        self.output_dir = output_dir
        self.session = session
    
    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *args):
        self.logout()
    
    def __get_csrf_token(self):
        response = session.get(LOGIN_POPUP_URL)
        match = re.search("name=\'csrfmiddlewaretoken\' value=\'(.*)\'", response.text)
        return match.group(1)
    
    def login(self):
        logger.info('Trying to log in ...')        
        csrf_token = self.__get_csrf_token()
        payload = {'isSubmitted': 1, 'email': self.username, 'password': self.password,
                   'displayType': 'ajax', 'csrfmiddlewaretoken': csrf_token}
        response = session.post(LOGIN_URL, payload)

        access_token = response.cookies.get('access_token')
        client_id = response.cookies.get('client_id')

        response_text = response.text        
        
        if 'check your email and password' in response_text:            
            raise UdemyException('Wrong Username or Password!')

        elif access_token is None:            
            raise UdemyException('Couldn\'t fetch token!')            

        elif 'error' in response_text:            
            raise UdemyException('Found error in login page')

        session.set_auth_headers(access_token, client_id)
        logger.info("Login success.")
    
    def __get_course_id(self, course_url):
        if 'udemy.com/draft/' in course_url:
            course_id = course_url.split('/')[-1]
            logger.info("Found draft...id: %s", course_id)
            return course_id
        
        response = session.get(course_url)
        response_text = response.text

        if 'data-purpose="take-this-course-button"' in response_text:            
            raise UdemyException('You\'re not enrolled in this course')
        
        logger.debug('Searching course id...')

        matches = re.search(r'data-course-id="(\d+)"', response_text, re.IGNORECASE)
        if matches:
            course_id = matches.groups()[0]
        else:
            matches = re.search(r'property="og:image"\s+content="([^"]+)"', response_text, re.IGNORECASE)
            course_id = matches.groups()[0].rsplit('/', 1)[-1].split('_', 1)[0] if matches else None

        if not course_id:
            raise UdemyException('Course id not found!')
        else:
            logger.info('Found course id: %s', course_id)

        return course_id

    def __get_course_title(self, course_id):        
        course_title_url = COURSE_TITLE_URL.format(course_id=course_id)
        course_title_data = session.get(course_title_url).json()
        course_title = course_title_data['title']
        logger.info('Found course title: %s', course_title)
        return course_title

    def __parse_video_url(self, lecture_id, hd=False):
        '''A hacky way to find the json used to initalize the swf object player'''
        embed_url = 'https://www.udemy.com/embed/{0}'.format(lecture_id)
        html = session.get(embed_url).text

        data = re.search(r'\$\("#player"\).jwplayer\((.*?)\);.*</script>', html,
                        re.MULTILINE | re.DOTALL).group(1)
        video = json.loads(data)

        if 'playlist' in video and 'sources' in video['playlist'][0]:
            if hd:
                for source in video['playlist'][0]['sources']:
                    if '720' in source['label'] or 'HD' in source['label']:
                        return source['file']

            # The 360p case and fallback if no HD version
            source = video['playlist'][0]['sources'][0]
            return source['file']
        else:
            print("Failed to parse video url")
            return None

    def __get_data_links(self, course_id):
        course_url = 'https://www.udemy.com/api-1.1/courses/{0}/curriculum?fields[lecture]=@min,completionRatio,progressStatus&fields[quiz]=@min,completionRatio'.format(course_id)
        course_data = session.get(course_url).json()
        logger.info('Found data: %s', course_data)

        # chapter = None
        # video_list = []

        # lecture_number = 1
        # chapter_number = 0        
        # for item in course_data:
        #     if item['__class'] == 'chapter':
        #         chapter = item['title']
        #         chapter_number += 1
        #     elif item['__class'] == 'lecture' and item['assetType'] == 'Video':
        #         lecture = item['title']
        #         try:
        #             lecture_id = item['id']
        #             video_url = self.__parse_video_url(lecture_id, hd)
        #             video_list.append({'chapter': chapter,
        #                             'lecture': lecture,
        #                             'video_url': video_url,
        #                             'lecture_number': lecture_number,
        #                             'chapter_number': chapter_number})
        #         except:
        #             print('Cannot download lecture "%s"' % (lecture))
        #         lecture_number += 1
        return ''

    def logout(self):
        logger.info('Logged Out!')
        time.sleep(1)

    def analyze(self):
        logger.info('Analyzing the course ...')
        course_id = self.__get_course_id(self.course_url)
        course_title = self.__get_course_title(course_id)
        data_links = self.__get_data_links(course_id)
        logger.info('data links: %s', data_links)

    def download(self):
        logger.info('Downloading files ...')
        time.sleep(5)
        logger.info('Downloaded all files.')
