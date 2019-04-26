from . import __title__
from .exceptions import UdemyException
from . import COURSE_TITLE_URL, COURSE_INFO_URL, GET_LECTURE_URL
from . import logger
import re

class Course(object):
    def __init__(self, course_link, session):
        self.course_link = course_link
        self.session = session
        self.course_id = self.__get_course_id(self.course_link)

    def __get_course_id(self, course_url):
        if 'udemy.com/draft/' in course_url:
            course_id = course_url.split('/')[-1]
            logger.debug("Found draft...id: %s", course_id)
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
            logger.debug('Found course id: %s', course_id)

        return course_id

    def get_course_title(self):
        course_title_url = COURSE_TITLE_URL.format(course_id=self.course_id)
        course_title_data = self.session.get(course_title_url).json()
        course_title = course_title_data['title']
        logger.debug('Found course title: %s', course_title)
        return course_title

    def get_course_data(self, quality):        
        course_url = COURSE_INFO_URL.format(course_id=self.course_id)
        course_data = self.session.get(course_url).json()

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
                    data_urls, data_type = self.__extract_lecture_url(self.course_id, lecture_id, quality)                   

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
                        'course_id': self.course_id,
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
                    logger.debug('Cannot download lecture "%s": "%s"', lecture, e)

                lecture_number += 1        
        return data_list

    def __extract_lecture_url(self, course_id, lecture_id, quality):        
        get_url = GET_LECTURE_URL.format(course_id=course_id, lecture_id=lecture_id)
        lecture_info = self.session.get(get_url).json()
        
        if lecture_info['asset']['download_urls']:
            logger.debug('Found videos for lecture: %s', lecture_id)
            dict_videos = {}
            for video in lecture_info['asset']['download_urls']['Video']:
                dict_videos[video['label']] = video['file']

            return (dict_videos[quality], 'Video')
        else:            
            logger.debug("Couldn't extract lecture url: %s", lecture_id)
            return (None, None)
    