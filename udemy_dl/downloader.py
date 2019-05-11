from . import logger
from .utils import unescape
import os
import subprocess
import requests

class Downloader():
    def __init__(self, course_data, root_dir):
        self.course_data = course_data
        self.root_dir = root_dir

    def __create_directory(self, dir_name):
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            pass


    def download(self):        
        self.__create_directory(self.root_dir)

        current_chapter = 0
        for data in self.course_data:
            if current_chapter < data['chapter_number']:
                current_chapter += 1
                dir_name = '{0:02d} - {1}'.format(current_chapter, data['chapter'])
                directory = os.path.join(self.root_dir, unescape(dir_name))
                self.__create_directory(directory)
            
            if data['data_type'] == 'Video':
                link = data['data_urls']
                filename = '{0:02d} - {1}.mp4'.format(data['lecture_number'], data['lecture'])
                self.__get_data(directory, link, unescape(filename))
            
            if data['attached_info']['attached_list']:
                """ Download attachments """                
                attachments = data['attached_info']['attached_list']
                for attachment in attachments:
                    link = attachment['link']
                    filename = attachment['filename']
                    self.__get_data(directory, link, unescape(filename))                

    def __get_data(self, directory, link, filename):        
        os.chdir(directory)
        logger.info('Downloading lecture: %s', filename)
        self.__curl_dl(link, filename)

    def __curl_dl(self, link, filename):
        command = ['curl', '-C', '-', link, '-o', filename, '--progress-bar']

        cert_path = requests.certs.where()
        if cert_path:
            command.extend(['--cacert', cert_path])
        else:
            command.extend(['--insecure'])
        subprocess.call(command)
    