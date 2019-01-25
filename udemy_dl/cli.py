import argparse
import logging
import getpass
import sys
import os

from .udemy_dl import UdemyDL, UdemyDLException
from . import __version__, __title__

logger = logging.getLogger(__title__)

class Cli:
    def __init__(self):
        self.argparser = self.create_argparser()


    def create_argparser(self):
        parser = argparse.ArgumentParser(
            description='Download all videos for a udemy course',
            prog=__title__
        )
        parser.add_argument(
            'link', 
            help='Link for udemy course',
            action='store'
        )
        parser.add_argument(
            '-u', '--username',
            help='Username/Email',
            default=None,
            action='store'
        )
        parser.add_argument(
            '-p', '--password',
            help='Password',
            default=None,
            action='store'
        )
        parser.add_argument(
            '-o', '--output-dir',
            help='Output directory',
            default=None,
            action='store'
        )
        parser.add_argument(
            '-v', '--version',
            help='Display the version of udemy-dl and exit',
            action='version',
            version='%(prog)s {version}'.format(version=__version__)
        )
        return parser

    def main(self):
        args = vars(self.argparser.parse_args())

        username = args['username']
        password = args['password']
        
        if not username:
            username = input("Username / Email : ")

        if not password:
            password = getpass.getpass(prompt='Password: ')

        link = args['link'].rstrip('/')

        if args['output_dir']:            
            output_dir = os.path.normpath(args['output_dir'])
        else:            
            output_dir = os.path.join(".", link.rsplit('/', 1)[1])

        try:
            with UdemyDL(link, username, password, output_dir) as dl:
                dl.analyze()
        except UdemyDLException as e:
            print(e)

        except KeyboardInterrupt:
            logger.error("User interrupted the process, exiting...")

        except Exception as e:
            logger.error('Unknown Exception')
            logger.exception(e)
            logger.info(
                'some text'
            )
        finally:
            sys.exit(1)


def main():
    Cli().main()
