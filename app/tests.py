import os
import sys

from pytube import YouTube

from app.generic_util import ret_date_format


def progress_callback(self, stream, chunk, bytes_remaining):
    # print(stream, chunk, file_handler, bytes_remaining)
    progress = (100 * (self._stream.filesize - bytes_remaining)) / self._stream.filesize
    progress_fmt = ("\rDownloading : {:00.0f}% ...".format(progress))
    self.set_progress_bar(progress)
    sys.stdout.write(progress_fmt)
    sys.stdout.flush()


def complete_callback(stream, file_path):
    print('Complete!')


if __name__ == '__main__':
    URL = 'https://www.youtube.com/watch?v=EecYFlPPVLQ'
    DESKTOP_DIR = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    yt = YouTube(
        url = URL,
        # on_progress_callback = progress_callback,
        on_complete_callback = complete_callback,
    )
    # print(yt)
    # pprint(yt.streams.all())
    stream = yt.streams.filter(type = 'audio', audio_codec = 'mp4a.40.2').last()
    stream.download(
        output_path = DESKTOP_DIR,
        filename = yt.title,
        filename_prefix = ret_date_format() + '_'
    )
