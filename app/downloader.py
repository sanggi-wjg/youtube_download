import sys
import threading

from pytube import YouTube

from app.generic_util import ret_date_format


class YouTubeDownloader(threading.Thread):
    """
    https://python-pytube.readthedocs.io/en/latest/api.html#stream-object
    """

    def __init__(self, url):
        super().__init__()
        self._YT = YouTube(url, on_progress_callback = self.progress_callback)
        self._stream = None

    ##############################################################################################################################

    def show_stream_all(self):
        for s in self._YT.streams.filter(progressive = True).all():
            print(s)

    ##############################################################################################################################

    def progress_callback(self, stream, chunk, file_handler, bytes_remaining):
        # print(stream, chunk, file_handler, bytes_remaining)
        progress = (100 * (self._stream.filesize - bytes_remaining)) / self._stream.filesize
        progress_fmt = ("\rDownloading : {:00.0f}% ...".format(progress))
        self._set_progress_bar(progress)
        sys.stdout.write(progress_fmt)
        sys.stdout.flush()

    ##############################################################################################################################

    def download_audio(self, save_path, set_progress_text, set_progress_bar):
        self._stream = self._YT.streams.get_audio_only()
        print('[+] (Start) ' + self._YT.title + ' Audio Download')
        self._set_progress_bar = set_progress_bar
        set_progress_text('[+] (Start) ' + self._YT.title + ' Audio Download')

        if not self._stream:
            raise ValueError

        final_path = self._stream.download(save_path, '.', self._YT.title + '_' + ret_date_format())
        print('\n[+] (Finish) Audio Download : ' + final_path)
        set_progress_text('[+] (Finish) Audio Download : ' + final_path)

    ##############################################################################################################################

    def download_video(self, save_path, set_progress_text, set_progress_bar):
        self._stream = self._YT.streams.filter(only_video = True, progressive = True, mime_type = 'video/mp4', type = 'video').order_by('resolution').last()
        print('[+] (Start) ' + self._YT.title + ' Video Download')
        self._set_progress_bar = set_progress_bar
        set_progress_text('[+] (Start) ' + self._YT.title + ' Video Download')

        if not self._stream:
            raise ValueError

        final_path = self._stream.download(save_path, '.', self._YT.title + '_' + ret_date_format())
        print('\n[+] (Finish) Video Download : ' + final_path)
        set_progress_text('[+] (Finish) Video Download : ' + final_path)

    ##############################################################################################################################


# if __name__ == '__main__':
#     _YTD = YouTubeDownloader('https://youtu.be/9SeNy3TzA-Y?list=PLFv3ZQw-ZPxi0H9oZp_lIsmak7bu_lcrK')
#     _YTD.show_stream_all()
