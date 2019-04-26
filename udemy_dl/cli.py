from . import __title__
from .argparser import parser
from .utils import sys_info
from .udemy_download import UdemyDownload
from .exceptions import UdemyException
import logging
import getpass
import os
import sys

logger = logging.getLogger(__title__)

class Cli:

    LOG_FORMAT_CONSOLE = '%(levelname)-8s %(message)s'

    def __init__(self):
        self.argparser = parser

    def __get_log_handler(self, error_level, formatter,
                    handler, handler_args={}):
        log_handler = handler(**handler_args)
        log_handler.setLevel(error_level)
        log_handler.setFormatter(logging.Formatter(formatter))
        return log_handler

    def __get_console_log_handler(self, error_level):
        return self.__get_log_handler(
            error_level, self.LOG_FORMAT_CONSOLE,
            logging.StreamHandler
        )

    def __init_logger(self, error_level=logging.INFO):
        logger.setLevel(error_level)
        logger.addHandler(self.__get_console_log_handler(error_level))
    
    def __generate_sys_info_log(self, sys_info):
        logger.debug('Running on:')
        logger.debug('Python: {}'.format(sys_info['python']))
        logger.debug('Platform: {}'.format(sys_info['platform']))
        logger.debug('OS: {}'.format(sys_info['os']))

    def run(self):
        args = vars(self.argparser.parse_args())

        link = args['link']
        username = args['username']
        password = args['password']
        debug = args['debug']
        quality = args['video_quality']
        
        if not username:
            username = input("Username / Email : ")

        if not password:
            password = getpass.getpass()            

        sys_information = sys_info()

        if debug:
            self.__init_logger(logging.DEBUG)
            self.__generate_sys_info_log(sys_information)
        else:
            self.__init_logger()

        if args['output']:
            output_dest = os.path.normpath(args['output'])            
        else:
            course_slug = link.rsplit('/', 1)[1]
            output_dest = os.path.normpath(course_slug)           

        output_dir = os.path.abspath(output_dest)        
        logger.debug('Downloading course to: %s', output_dir)
        logger.debug('Downloading with quality: %s', quality)

        try:
            with UdemyDownload(link, username, password, output_dir, quality) as ud:                
                ud.analyze()
                ud.download()
        except UdemyException as ue:
            logger.error(ue.args[0])
        except KeyboardInterrupt:
            logger.error('User interrupted the process, exiting...')
        except Exception as e:
            logger.error('Unknown Exception')
            logger.exception(e)
        finally:
            sys.exit(1)
