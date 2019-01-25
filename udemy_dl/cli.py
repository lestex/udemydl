import argparse
import logging
import getpass
import sys
import time

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
            '--lecture-start',
            help='Lecture to start at (default is 1)',
            default=1,
            action='store'
        )
        parser.add_argument(
            '--lecture-end',
            help='Lecture to end at (default is last)',
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
            password = getpass.getpass()

        try:
            with UdemyDL(args['link'], username, password) as udl:
                time.sleep(5)
        except UdemyDLException as lae:
            print(lae.args[0])

        except KeyboardInterrupt:
            print("User interrupted the process, exiting...")

        finally:
            sys.exit(1)


def main():
    Cli().main()

if __name__ == "__main__":
    main()
