#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import sys
import re
import os
import json

import time

from .session import session
#from .download import download, DLException
from udemy_dl import __version__

class UdemyDLException(Exception):
    pass

class UdemyDL:
    def __init__(self, *args):
        pass

    def __enter__(self):        
        return self
    
    def __exit__(self, *args):
        pass

    def analyze(self):
        time.sleep(5)


def get_csrf_token():
    response = session.get('https://www.udemy.com/join/login-popup')
    match = re.search("name=\'csrfmiddlewaretoken\' value=\'(.*)\'", response.text)
    return match.group(1)

def login(username, password):
    login_url = 'https://www.udemy.com/join/login-popup/?displayType=ajax&display_type=popup&showSkipButton=1&returnUrlAfterLogin=https%3A%2F%2Fwww.udemy.com%2F&next=https%3A%2F%2Fwww.udemy.com%2F&locale=en_US'
    csrf_token = get_csrf_token()
    payload = {'isSubmitted': 1, 'email': username, 'password': password,
               'displayType': 'ajax', 'csrfmiddlewaretoken': csrf_token}
    response = session.post(login_url, payload)

    access_token = response.cookies.get('access_token')
    client_id = response.cookies.get('client_id')
    session.set_auth_headers(access_token, client_id)

    response = response.text
    if 'error' in response:
        print(response)
        # TODO throw exception


def get_course_id(course_link):
    response = session.get(course_link)
    matches = re.search('data-courseid="(\d+)"', response.text, re.IGNORECASE)
    return matches.groups()[0] if matches else None


def parse_video_url(lecture_id, hd=False):
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


def get_video_links(course_id, lecture_start, lecture_end, hd=False):
    course_url = 'https://www.udemy.com/api-1.1/courses/{0}/curriculum?fields[lecture]=@min,completionRatio,progressStatus&fields[quiz]=@min,completionRatio'.format(course_id)
    course_data = session.get(course_url).json()

    chapter = None
    video_list = []

    lecture_number = 1
    chapter_number = 0
    # A udemy course has chapters, each having one or more lectures
    for item in course_data:
        if item['__class'] == 'chapter':
            chapter = item['title']
            chapter_number += 1
        elif item['__class'] == 'lecture' and item['assetType'] == 'Video':
            lecture = item['title']
            if valid_lecture(lecture_number, lecture_start, lecture_end):
                try:
                    lecture_id = item['id']
                    video_url = parse_video_url(lecture_id, hd)
                    video_list.append({'chapter': chapter,
                                       'lecture': lecture,
                                       'video_url': video_url,
                                       'lecture_number': lecture_number,
                                       'chapter_number': chapter_number})
                except:
                    print('Cannot download lecture "%s"' % (lecture))
            lecture_number += 1
    return video_list


def valid_lecture(lecture_number, lecture_start, lecture_end):
    if lecture_start and lecture_end:
        return lecture_start <= lecture_number <= lecture_end
    elif lecture_start:
        return lecture_start <= lecture_number
    else:
        return lecture_number <= lecture_end


def sanitize_path(s):
    return "".join([c for c in s if c.isalpha() or c.isdigit() or c in ' .-_,']).rstrip()


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_video(directory, filename, link):
    print('Downloading %s  ' % (filename.encode('utf-8')))
    previous_dir = os.getcwd()
    mkdir(directory)
    os.chdir(directory)
    try:
        download(link, filename)
    except DLException as e:
        print('Couldn\'t download this lecture: {0}'.format(e))
    os.chdir(previous_dir)
    print('\n'),

def udemy_dl(username, password, course_link, lecture_start, lecture_end, dest_dir=""):
    login(username, password)

    course_id = get_course_id(course_link)
    if not course_id:
        print('Failed to get course ID')
        return

    for video in get_video_links(course_id, lecture_start, lecture_end, hd=True):
        directory = '%02d %s' % (video['chapter_number'], video['chapter'])
        directory = sanitize_path(directory)

        if dest_dir:
            directory = os.path.join(dest_dir, directory)

        filename = '%03d %s.mp4' % (video['lecture_number'], video['lecture'])
        filename = sanitize_path(filename)

        get_video(directory, filename, video['video_url'])

    session.get('http://www.udemy.com/user/logout')
