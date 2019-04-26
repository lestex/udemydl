from . import __title__
from .exceptions import UdemyException
from . import COURSE_TITLE_URL, COURSE_INFO_URL, GET_LECTURE_URL, ATTACHMENT_URL, GET_LECTURE_URL
from . import logger
import re

class Course(object):
    def __init__(self, course_link, session):
        self.course_link = course_link
        self.session = session
        self.course_id = self.__get_course_id(self.course_link)

    def __get_course_id(self, course_url):
        """Extract course_id from the course page"""
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
            logger.debug('Found course id: %s', course_id)

        return course_id

    def get_course_data(self, quality):        
        course_url = COURSE_INFO_URL.format(course_id=self.course_id)
        json_source = self.session.get(course_url).json()

        chapter = None
        course_data = []
        supported_asset_type = ['Video', 'VideoMashup']
        supported_supplementary_assets = ['File']

        lecture_number = 1
        chapter_number = 0
        item_count = 0

        for item in json_source['results']:
            item_count += 1
            lecture = item['title']
            lecture_id = item['id']           

            if item['_class'] == 'chapter':                
                chapter = item['title']
                chapter_number += 1

            elif item['_class'] == 'lecture' and item['asset']['asset_type'] in supported_asset_type:                           
                try:
                    data_urls, data_type = self.__extract_lecture_url(self.course_id, lecture_id, quality)                   

                    if data_urls is None:
                        lecture_number += 1
                        continue

                    attached_list = []
                    if item.get('supplementary_assets'):
                        for asset in item['supplementary_assets']:
                            if asset['asset_type'] in supported_supplementary_assets:
                                attached_list.append({
                                    'filename': asset['filename'],
                                    'id': asset['id'],
                                    'link': self.__parse_file(self.course_id, lecture_id, asset['id'])
                                })

                    attached_info = {
                        'course_id': self.course_id,
                        'lecture_id': lecture_id,
                        'attached_list': attached_list
                    }

                    course_data.append({
                        'chapter': chapter,
                        'lecture': lecture,
                        'data_urls': data_urls,
                        'data_type': data_type,
                        'attached_info': attached_info,
                        'lecture_number': int(lecture_number),
                        'chapter_number': int(chapter_number)
                    })
                except Exception as e:
                    logger.debug('Cannot download lecture "%s": "%s"', lecture, e)

                lecture_number += 1        
        return course_data

    def __extract_lecture_url(self, course_id, lecture_id, quality):
        """Extracting Video URLs from json_source for type File."""
        get_url = GET_LECTURE_URL.format(course_id=course_id, lecture_id=lecture_id)
        json_source = self.session.get(get_url).json()
        
        dict_videos = {}

        if json_source['asset']['download_urls']:
            logger.debug('Found videos marked as downloadable: %s', lecture_id)
            for video in json_source['asset']['download_urls']['Video']:
                dict_videos[video['label']] = video['file']
            return (dict_videos[quality], 'Video')

        elif json_source['asset']['stream_urls']:
            logger.debug('Falling back to stream urls: %s', lecture_id)
            for video in json_source['asset']['stream_urls']['Video']:
                dict_videos[video['label']] = video['file']
            return (dict_videos[quality], 'Video')

        else:            
            logger.debug("Couldn't extract lecture url: %s, the lecture might be set as not downloadable", lecture_id)
            return (None, None)

    def __parse_file(self, course_id, lecture_id, attachment_id):
        """Extracting URL from json_source for type File."""
        get_url = ATTACHMENT_URL.format(course_id=course_id, lecture_id=lecture_id, attachment_id=attachment_id)
        json_source = self.session.get(get_url).json()
        for f in json_source['download_urls']['File']:
            if f['label'] == 'download':
                return f['file']
            else:
                logger.debug("Skipped. Couldn't fetch File!")
                return None
    