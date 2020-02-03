import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QGridLayout, QLabel, QLineEdit, QGroupBox, QProgressBar, QTextEdit, QPushButton
from pytube.exceptions import RegexMatchError

from app.downloader import YouTubeDownloader
from app.setting import APP_NAME, ICON_PATH, DESKTOP_DIR

"""
http://codetorial.net/pyqt5/widget/qlineedit_advanced.html
https://wiki.python.org/moin/PyQt/SampleCode
https://pythonprogramminglanguage.com/pyqt-tutorials
https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/

Combine Video + Audio = https://ffmpeg.org/ffmpeg.html

Sample YouTube Link : https://youtu.be/TdeY6cA3j2Q?list=PLFv3ZQw-ZPxi0H9oZp_lIsmak7bu_lcrK
"""


class AppWindow(QWidget):

    def __init__(self):
        super().__init__()
        self._default()
        self._center()
        self._layout()
        self.show()

    def _default(self):
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(800, 500)

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    ##############################################################################################################################

    def _layout(self):
        self._layout_download()
        self._layout_youtube()
        self._layout_progress()

        self.layout = QGridLayout()
        self.layout.addWidget(self._download_group, 0, 0)
        self.layout.addWidget(self._youtube_group, 1, 0)
        self.layout.addWidget(self._progress_group, 2, 0)
        self.setLayout(self.layout)

    ##############################################################################################################################

    def _layout_download(self):
        self._download_group = QGroupBox('Download')
        self._download_label = QLabel('Folder:')
        self._download_lineEdit = QLineEdit(DESKTOP_DIR)

        self._download_layout = QGridLayout()
        self._download_layout.addWidget(self._download_label, 0, 0)
        self._download_layout.addWidget(self._download_lineEdit, 0, 1)
        self._download_group.setLayout(self._download_layout)

    def get_download_path(self):
        return str(self._download_lineEdit.text())

    ##############################################################################################################################

    def _layout_youtube(self):
        self._youtube_group = QGroupBox('YouTube')
        self._youtube_label = QLabel('Link:')
        self._youtube_lineEdit = QLineEdit()
        self._youtube_btn_audio = QPushButton('Audio', self)
        self._youtube_btn_audio.clicked.connect(self.click_btn_audio)
        self._youtube_btn_video = QPushButton('Video', self)
        self._youtube_btn_video.clicked.connect(self.click_btn_video)

        self._youtube_layout = QGridLayout()
        self._youtube_layout.addWidget(self._youtube_label, 0, 0)
        self._youtube_layout.addWidget(self._youtube_lineEdit, 0, 1)
        self._youtube_layout.addWidget(self._youtube_btn_audio, 0, 2)
        self._youtube_layout.addWidget(self._youtube_btn_video, 0, 3)
        self._youtube_group.setLayout(self._youtube_layout)

    def get_youtube_link(self):
        link = str(self._youtube_lineEdit.text()).strip()
        self._youtube_lineEdit.setText(link)
        return link

    def click_btn_audio(self):
        download_path = self.get_download_path()
        youtube_link = self.get_youtube_link()

        if not download_path:
            self.set_progress_text('Please, Input Download Path')
            return

        if not youtube_link:
            self.set_progress_text('Please, Input YouTube Link')
            return

        try:
            _YTD = YouTubeDownloader(youtube_link)
            _YTD.download_audio(download_path, self.set_progress_text, self.set_progress_bar)
            QApplication.processEvents()

        except RegexMatchError:
            self.set_progress_text('Invalid YouTube Link')

        except Exception as e:
            print(e.__class__, e.__str__())
            self.set_progress_text(e.__str__())

    def click_btn_video(self):
        download_path = self.get_download_path()
        youtube_link = self.get_youtube_link()

        if not download_path:
            self.set_progress_text('Please, Input Download Path')
            return

        if not youtube_link:
            self.set_progress_text('Please, Input YouTube Link')
            return

        try:
            _YTD = YouTubeDownloader(youtube_link)
            _YTD.download_video(download_path, self.set_progress_text, self.set_progress_bar)
            QApplication.processEvents()

        except RegexMatchError:
            self.set_progress_text('Invalid YouTube Link')

        except Exception as e:
            print(e.__class__, e.__str__())
            self.set_progress_text(e.__str__())

    ##############################################################################################################################

    def _layout_progress(self):
        self._progress_group = QGroupBox('Progress')
        self._progress_bar = QProgressBar()
        self._progress_textEdit = QTextEdit()

        self._progress_layout = QGridLayout()
        self._progress_layout.addWidget(self._progress_bar, 0, 0)
        self._progress_layout.addWidget(self._progress_textEdit, 1, 0)
        self._progress_group.setLayout(self._progress_layout)

    def set_progress_bar(self, value):
        self._progress_bar.setValue(value)

    def set_progress_text(self, msg = ''):
        current_text = str(self._progress_textEdit.toPlainText())
        if current_text:
            self._progress_textEdit.setText(current_text + '\n' + msg)
        else:
            self._progress_textEdit.setText(msg)
    ##############################################################################################################################


##############################################################################################################################

if __name__ == '__main__':
    try:
        app = QApplication([])
        window = AppWindow()
        sys.exit(app.exec_())

    except Exception as e:
        print(e.__traceback__.tb_lineno, e.__str__())
