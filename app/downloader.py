import sys

from pytube import YouTube


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
        for s in self._YT.streams.filter(progressive = True).all():
            print(s)

    ##############################################################################################################################

    def _progress_callback(self, stream, chunk, file_handler, bytes_remaining):
        # print(stream, chunk, file_handler, bytes_remaining)
        progress = (100 * (self._stream.filesize - bytes_remaining)) / self._stream.filesize
        progress_fmt = ("\rDownloading : {:00.0f}% ...".format(progress))
        self.set_progress_bar(progress)
        sys.stdout.write(progress_fmt)
        sys.stdout.flush()

    ##############################################################################################################################
    def _find_stream(self, type):
        if type == 'audio':
            self._stream = self._YT.streams.get_audio_only()
        elif type == 'video':
            self._stream = self._YT.streams.filter(only_video = True, progressive = True, mime_type = 'video/mp4', type = 'video').order_by('resolution').last()
        else:
            raise ValueError('Invalid type')

        if not self._stream:
            raise ValueError('Empty _stream')

    ##############################################################################################################################

    def download_stream(self, type, path):
        self._find_stream(type)
        print('[+] Find Stream ' + self._YT.title, self._stream)

        final_path = self._stream.download(path, self._YT.title)
        print('\n[+] (Finish) Download : ' + final_path)
