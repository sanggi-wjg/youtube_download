import logging
import sys

from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QGridLayout, QLabel, QLineEdit, QGroupBox, QProgressBar, QTextEdit, QPushButton
from pytube.exceptions import RegexMatchError

from app.downloader import YouTubeDownloader
from app.setting import APP_NAME, ICON_PATH, DESKTOP_DIR
from app.worker import Worker


class AppWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()
        print("Multi threading with maximum {} threads".format(self.threadpool.maxThreadCount()))

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
        path = str(self._download_lineEdit.text()).strip()
        self._download_lineEdit.setText(path)
        return path

    ##############################################################################################################################

    def _layout_youtube(self):
        self._youtube_group = QGroupBox('YouTube')
        self._youtube_label = QLabel('Link:')
        # self._youtube_lineEdit = QLineEdit('https://youtu.be/TdeY6cA3j2Q?list=PLFv3ZQw-ZPxi0H9oZp_lIsmak7bu_lcrK')
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

    ##############################################################################################################################

    def worker_output(self, s):
        print(s)

    def worker_execute(self, progress_callback, *args, **kwargs):
        print(progress_callback)
        print(args, kwargs)

        url = kwargs.pop('url')
        download_type = kwargs.pop('download_type')
        download_path = kwargs.pop('download_path')

        Downloader = YouTubeDownloader(url, self.set_progress_bar)
        Downloader.download_stream(download_type, download_path)
        # for n in range(0, 5):
        #     time.sleep(1)
        #     progress_callback.emit(n * 100 / 4)

        return True

    def thread_complete(self):
        # self.set_btn_audio_enabled()
        # self.set_btn_video_enabled()
        self._youtube_btn_audio.setEnabled(True)
        self._youtube_btn_video.setEnabled(True)
        print('[+] Download To ' + self.get_download_path())

    ##############################################################################################################################

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
            self._youtube_btn_audio.setDisabled(True)
            self._youtube_btn_video.setDisabled(True)
            self.set_progress_text('[+] Start Download : ' + youtube_link)
            self.set_progress_text('[+] Download Path : ' + download_path)

            worker = Worker(self.worker_execute, url = youtube_link, download_type = 'audio', download_path = download_path)
            worker.signals.result.connect(self.worker_output)
            worker.signals.progress.connect(self.set_progress_bar)
            worker.signals.finished.connect(self.thread_complete)

            self.threadpool.start(worker)

        except (TypeError, KeyError, ValueError) as le:
            print(le.__class__, le.__str__())
            # self.set_progress_text('Logic Error Raised')

        except RegexMatchError:
            self.set_progress_text('Invalid YouTube Link')

        except Exception as e:
            print(e.__class__, e.__str__())
            # self.set_progress_text(e.__str__())

    ##############################################################################################################################

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
            self.set_btn_audio_enabled(False)
            self.set_btn_video_enabled(False)
            self.set_progress_text('[+] Start Download : ' + youtube_link)
            self.set_progress_text('[+] Download Path : ' + download_path)

            worker = Worker(self.worker_execute, url = youtube_link, download_type = 'video', download_path = download_path)
            worker.signals.result.connect(self.worker_output)
            worker.signals.progress.connect(self.set_progress_bar)
            worker.signals.finished.connect(self.thread_complete)

            self.threadpool.start(worker)

        except (TypeError, KeyError, ValueError) as le:
            print(le.__class__, le.__str__())
            # self.set_progress_text('Logic Error Raised')

        except RegexMatchError:
            self.set_progress_text('Invalid YouTube Link')

        except Exception as e:
            print(e.__class__, e.__str__())
            # self.set_progress_text(e.__str__())

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
        try:
            self._progress_bar.setValue(value)

        except Exception as e:
            print(e.__traceback__.tb_lineno, e.__str__())

    def set_progress_text(self, msg = ''):
        try:
            current_text = str(self._progress_textEdit.toPlainText())
            if current_text:
                self._progress_textEdit.setText(current_text + '\n' + msg + '.')
            else:
                self._progress_textEdit.setText(msg + '.')

        except Exception as e:
            print(e.__traceback__.tb_lineno, e.__str__())
    ##############################################################################################################################


##############################################################################################################################

if __name__ == '__main__':
    logging.getLogger('pytube').setLevel(logging.DEBUG)

    app = QApplication([])
    window = AppWindow()
    sys.exit(app.exec_())
