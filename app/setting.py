import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESKTOP_DIR = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
ICON_PATH = BASE_DIR + '/assets/fav.png'

APP_NAME = 'YouTube Downloader'
