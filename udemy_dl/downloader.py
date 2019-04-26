from . import logger
import os

class Downloader():
    def __init__(self, course_data, output_dir):
        self.course_data = course_data
        self.output_dir = output_dir

    def __create_directory(self, dir_name):
        os.mkdir(dir_name)        

    def download(self):        
        self.__create_directory(self.output_dir)

        current_chapter = 1
        for data in self.course_data:
            if current_chapter < data['chapter_number']:
                current_chapter += 1            
            dir_name = '{0:02d} - {1}'.format(current_chapter, data['chapter'])
            directory = os.path.join(self.output_dir, dir_name)
            self.__get_data(directory, data)


    def __get_data(self, directory, data):
        logger.info('Downloading to directory: %s ', directory)
        # self.__create_directory(directory)
        # os.chdir(directory)
        # # logger.info('-- %s Lecture: %s ', d['lecture_number'], d['lecture'])
        # # logger.info('---- Lecture link: %s ',d['data_urls'])
        # # if d['attached_info']['attached_list']:
        # #     logger.info('-------- Attachment link: %s ',d['attached_info']['attached_list'][0]['link'])
    