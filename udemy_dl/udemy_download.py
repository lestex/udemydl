from . import __title__
from .session import session
from .exceptions import UdemyException
from .course import Course
import time
import logging
import re
import sys
import json

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

logger = logging.getLogger(__title__)

LOGIN_URL = 'https://www.udemy.com/join/login-popup/?displayType=ajax&display_type=popup&showSkipButton=1&returnUrlAfterLogin=https%3A%2F%2Fwww.udemy.com%2F&next=https%3A%2F%2Fwww.udemy.com%2F&locale=en_US'
LOGIN_POPUP_URL = 'https://www.udemy.com/join/login-popup'
LOGOUT_URL = 'http://www.udemy.com/user/logout'
COURSE_TITLE_URL = 'https://www.udemy.com/api-2.0/courses/{course_id}?fields[course]=title'
COURSE_INFO_URL = 'https://www.udemy.com/api-2.0/courses/{course_id}/cached-subscriber-curriculum-items?fields[asset]=@min,title,filename,asset_type,external_url,length&fields[chapter]=@min,description,object_index,title,sort_order&fields[lecture]=@min,object_index,asset,supplementary_assets,sort_order,is_published,is_free&fields[quiz]=@min,object_index,title,sort_order,is_published&page_size=550'
GET_LECTURE_URL = 'https://www.udemy.com/api-2.0/users/me/subscribed-courses/{course_id}/lectures/{lecture_id}?fields[asset]=@min,download_urls,external_url,slide_urls&fields[course]=id,is_paid,url&fields[lecture]=@default,view_html,course&page_config=ct_v4'
ATTACHMENT_URL = 'https://www.udemy.com/api-2.0/users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/supplementary-assets/{attachment_id}?fields[asset]=download_urls'

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

        self.session.set_auth_headers(access_token, client_id)
        logger.info("Login success.")
    
    def __get_course_id(self, course_url):
        if 'udemy.com/draft/' in course_url:
            course_id = course_url.split('/')[-1]
            logger.info("Found draft...id: %s", course_id)
            return course_id
        
        response = self.session.get(course_url)
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
        course_title_data = self.session.get(course_title_url).json()
        course_title = course_title_data['title']
        logger.info('Found course title: %s', course_title)
        return course_title

    def __get_data_links(self, course_id):        
        course_url = COURSE_INFO_URL.format(course_id=course_id)
        course_data = session.get(course_url).json()

        chapter = None
        data_list = []
        supported_asset_type = ['Video', 'VideoMashup']

        lecture_number = 1
        chapter_number = 0
        item_count = 0.0        

        for item in course_data['results']:
            item_count += 1
            lecture = item['title']
            lecture_id = item['id']           

            if item['_class'] == 'chapter':                
                chapter = item['title']
                chapter_number += 1

            elif item['_class'] == 'lecture' and item['asset']['asset_type'] in supported_asset_type:                           
                try:
                    data_urls, data_type = self.__extract_lecture_url(course_id, lecture_id)                   

                    if data_urls is None:
                        lecture_number += 1
                        continue

                    attached_list = []
                    if item.get('supplementary_assets'):
                        for asset in item['supplementary_assets']:
                            attached_list.append({
                                'filename': asset['filename'],
                                'id': asset['id']
                            })

                    attached_info = {
                        'course_id': course_id,
                        'lecture_id': lecture_id,
                        'attached_list': attached_list
                    }

                    data_list.append({
                        'chapter': chapter,
                        'lecture': lecture,
                        'data_urls': data_urls,
                        'data_type': data_type,
                        'attached_info': attached_info,
                        'lecture_number': int(lecture_number),
                        'chapter_number': int(chapter_number)
                    })
                except Exception as e:
                    logger.critical('Cannot download lecture "%s": "%s"', lecture, e)

                lecture_number += 1        
        return data_list

    def __extract_lecture_url(self, course_id, lecture_id, quality=None):        
        get_url = GET_LECTURE_URL.format(course_id=course_id, lecture_id=lecture_id)
        lecture_info = session.get(get_url).json()
        
        if lecture_info['asset']['download_urls']:
            logger.debug('Found Videos in course data - lecture_info')
            dict_videos = {}
            for video in lecture_info['asset']['download_urls']['Video']:
                dict_videos[video['label']] = video['file']

            if quality in ['720', '360']:
                return (dict_videos[quality], 'Video')
            else:
                return (dict_videos, 'Video')
        else:            
            logger.critical("Couldn't extract lecture url: %s", lecture_id)
            return (None, None)

    def logout(self):
        self.session.get(LOGOUT_URL)
        logger.info('Logged Out!')        

    def analyze(self):
        logger.info('Analyzing the course ...')
        course = Course(self.course_url, self.session)
        course_id = self.__get_course_id(self.course_url)
        course_title = self.__get_course_title(course_id)
        data_links = self.__get_data_links(course_id)
        logger.info('data links: %s', data_links)

    def download(self):
        logger.info('Downloading files ...')
        time.sleep(1)
        logger.info('Downloaded all files.')
