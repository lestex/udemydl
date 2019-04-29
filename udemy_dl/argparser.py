import argparse
from udemy_dl import __title__

parser = argparse.ArgumentParser(description='Download courses from Udemy.com', prog=__title__)
parser.add_argument('--debug', help='Enable debug mode', action='store_const', const=True, default=False)
parser.add_argument('link', help='Link for udemy course', action='store')
parser.add_argument('-u', '--username', help='Username / Email', default=None, action='store')
parser.add_argument('-p', '--password', help='Password', default=None, action='store')
parser.add_argument('-o', '--output', help='Output directory', default=None, action='store')
parser.add_argument('-q', '--video-quality', help='Select video quality 720, 480 (default is 720)', default='720', action='store')
