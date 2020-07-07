from pytube import Playlist

URL = 'https://www.youtube.com/playlist?list=PL-8zNJY17janVDAUaFr4adH85j-HlWy9g'

if __name__ == '__main__':
    playlist = Playlist(url = URL)
    print(playlist, type(playlist))
    print(playlist.playlist_url)

    print([v for v in playlist.videos])

    for video in playlist.videos:
        print(video.streams.all())
