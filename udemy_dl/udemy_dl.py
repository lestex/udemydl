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

class UdemyDLException(Exception):
    pass

class UdemyDL:
    def __init__(self, link, username, password, output_dir):
        self.username = username
        self.password = password
        self.link = link
        self.output_dir = output_dir
        self.course_id = self.get_course_id(link)

    def __enter__(self):
        self.login(self.username, self.password)
        return self
    
    def __exit__(self, *args):
        self.logout()

    def analyze(self):
        time.sleep(5)


    def get_csrf_token(self):
        response = session.get('https://www.udemy.com/join/login-popup')
        match = re.search("name=\'csrfmiddlewaretoken\' value=\'(.*)\'", response.text)        
        return match.group(1)

    def login(self, username, password):
        login_url = 'https://www.udemy.com/join/login-popup/?displayType=ajax&display_type=popup&showSkipButton=1&returnUrlAfterLogin=https%3A%2F%2Fwww.udemy.com%2F&next=https%3A%2F%2Fwww.udemy.com%2F&locale=en_US'
        csrf_token = self.get_csrf_token()
        payload = {'isSubmitted': 1, 'email': username, 'password': password,
                'displayType': 'ajax', 'csrfmiddlewaretoken': csrf_token}
        response = session.post(login_url, payload)

        access_token = response.cookies.get('access_token')
        client_id = response.cookies.get('client_id')
        session.set_auth_headers(access_token, client_id)

        response = response.text
        if 'error' in response:            
            raise UdemyDLException('could not authenticate')


    def get_course_id(self, course_link):
        response = session.get(course_link)        
        matches = re.search('data-clp-course-id="(\d+)"', response.text, re.IGNORECASE)        
        return matches.groups()[0] if matches else None

    def logout(self):
        session.get('http://www.udemy.com/user/logout')
