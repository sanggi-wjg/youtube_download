import os

"""
http://codetorial.net/pyqt5/widget/qlineedit_advanced.html
https://wiki.python.org/moin/PyQt/SampleCode
https://pythonprogramminglanguage.com/pyqt-tutorials
https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/

Combine Video + Audio = https://ffmpeg.org/ffmpeg.html

Sample YouTube Link
https://youtu.be/TdeY6cA3j2Q?list=PLFv3ZQw-ZPxi0H9oZp_lIsmak7bu_lcrK
"""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESKTOP_DIR = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
ICON_PATH = BASE_DIR + '/assets/fav.png'

APP_NAME = 'YouTube Downloader'
