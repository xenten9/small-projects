from typing import List, Union
from os import getcwd, path, remove, mkdir
import moviepy.editor as mpe # type: ignore
from time import time
import unicodedata
import re
from time import sleep

try:
    from pytube import YouTube # type: ignore
    from pytube.streams import Stream # type: ignore
except ModuleNotFoundError:
    print('python does not have module pytube')
    print('to install pytube open up a console and type:')
    print('<python installation path> -m pip install pytube')
    print('once installed try running again')
    exit()

def slugify(value: str, allow_unicode: bool = False) -> str:
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def get_urls() -> List[str]:
    if path.exists(rip_file):
        rip = open(rip_file, 'r')
        urls = rip.readlines()
        rip.close()
        return urls
    else:
        raise FileNotFoundError('rip file not found')

def complete(stream: Stream, file_path: Union[str, None]):
    if file_path is not None:
        print('pytube - <' + path.basename(file_path) + '> download complete')

def combine_audio(vidname: str, audname: str, outname: str, fps: int = 60):
    video = mpe.VideoFileClip(vidname)
    audio = mpe.AudioFileClip(audname)
    final = video.set_audio(audio)
    final.write_videofile(outname,fps=fps,codec='libx264')

def download_urls(urls: List[str], combine: bool = False):
    delete: List[str] = []
    for url in urls:
        print('url: {}'.format(url))
        if url[0] == '#':
            continue
        sleep(1.01)
        yt = YouTube(url, on_complete_callback=complete)
        #try:
        streams = yt.streams
        #except Exception as e:
        #    print(e)
        #    continue
        title = yt.title
        title = slugify(title)
        src_path = path.join(music_path, 'src')

        videotitle = title + ' - video'
        videofile = path.join(src_path, videotitle + '.mp4')
        if path.exists(videofile):
            remove(videofile)
        stream = streams.get_highest_resolution()
        if stream is not None:
            stream.download(src_path, videotitle)
        else:
            print('Stream returned None.')
            continue

        audiotitle = title + ' - audio'
        audiofile = path.join(src_path, audiotitle + '.mp4')
        if path.exists(audiofile):
            remove(audiofile)
        stream = streams.get_audio_only()
        if stream is not None:
            stream.download(src_path, audiotitle)
        else:
            print('Stream returned None.')
            continue

        del stream
        if combine:
            file = path.join(music_path, title + '.mp4')
            combine_audio(videofile, audiofile, file)

            delete.append(videofile)
            delete.append(audiofile)

    t = time()
    while len(delete) > 0:
        delete_copy = delete.copy()
        for file in delete_copy:
            try:
                remove(file)
                delete.remove(file)
            except ZeroDivisionError:
                pass
        if time() - t > 10:
            break

def main():
    download_urls(get_urls(), True)

if __name__ == '__main__':
    main_path = getcwd()
    if main_path[-6:] != 'loader':
        main_path = path.join(main_path, 'musicdownloader')
        if not path.exists(main_path):
            raise FileNotFoundError('unable to locate main directory')
    music_path = path.join(main_path, 'music')
    rip_file = path.join(main_path, 'rip.txt')
    if not path.exists(music_path):
        mkdir(music_path)
    if not path.exists(path.join(music_path, 'src')):
        mkdir(path.join(music_path, 'src'))
    if not path.exists(rip_file):
        rip = open(rip_file, 'w')
        rip.close()
    main()
