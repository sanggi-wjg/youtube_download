import sys

from pytube import YouTube

from app.generic_util import ret_date_format


class YouTubeDownloader:
    """
    https://python-pytube.readthedocs.io/en/latest/api.html#stream-object
    """

    def __init__(self, url, set_progress_bar):
        self._YT = YouTube(url, on_progress_callback = self._progress_callback)
        self._stream = None
        self.set_progress_bar = set_progress_bar

    ##############################################################################################################################

    def show_stream_all(self):
        for s in self._YT.streams.all():
            print(s)

    ##############################################################################################################################

    def _progress_callback(self, stream, chunk, bytes_remaining):
        # print(stream, chunk, file_handler, bytes_remaining)
        progress = (100 * (self._stream.filesize - bytes_remaining)) / self._stream.filesize
        progress_fmt = ("\rDownloading : {:00.0f}% ...".format(progress))
        self.set_progress_bar(progress)
        sys.stdout.write(progress_fmt)
        sys.stdout.flush()

    ##############################################################################################################################
    def _find_stream(self, type):
        # self.show_stream_all()
        if type == 'audio':
            self._stream = self._YT.streams.get_audio_only()
        elif type == 'video':
            self._stream = self._YT.streams.filter(only_video = True, progressive = False, mime_type = 'video/mp4', type = 'video').order_by('resolution').last()
        else:
            raise ValueError('Invalid type')

        if not self._stream:
            raise ValueError('Empty _stream')

    ##############################################################################################################################

    def download_stream(self, type, path):
        self._find_stream(type)
        print('[+] Find Stream ' + self._YT.title, self._stream)
        filename = '{}_{}'.format(ret_date_format(), self._YT.title)

        final_path = self._stream.download(path, filename)
        print('\n[+] (Finish) Download : ' + final_path)
