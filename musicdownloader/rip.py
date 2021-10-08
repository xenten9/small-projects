from typing import List, Union
from os import getcwd, path, remove, mkdir
import moviepy.editor as mpe  # type: ignore
from time import time
import unicodedata
import re

# Test for pytube existence
try:
    from pytube import YouTube  # type: ignore
    from pytube.streams import Stream  # type: ignore
except ModuleNotFoundError:
    print("python does not have module pytube")
    print("to install pytube open up a console and type:")
    print("<python installation path> -m pip install pytube")
    print("once installed try running again")
    exit()


# Used for naming system files
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
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


# Gets url's from a file
def get_urls() -> List[str]:
    """Will read the rip.txt file to see all links and returns a list."""
    if path.exists(rip_file):
        rip = open(rip_file, "r")
        urls = rip.readlines()
        rip.close()
        return urls
    else:
        raise FileNotFoundError("rip file not found")


# Prints when a download is complete
def complete(stream: Stream, file_path: Union[str, None]):
    """Notify's completion of a given download."""
    if file_path is not None:
        print("pytube - <" + path.basename(file_path) + "> download complete")


# Combines raw audio and video int one file
def combine_audio(vidname: str, audname: str, outname: str, fps: int = 60):
    """Takes in video and audio files and mixes them into one."""
    video = mpe.VideoFileClip(vidname)
    audio = mpe.AudioFileClip(audname)
    final: mpe.VideoFileClip = video.set_audio(audio)
    final.write_videofile(outname, fps=fps, codec="libx264")


# Takes a list of url's and downloads them from YouTube
def main(urls: List[str], combine: bool = False):
    """Will take each url and downlaod its coresponding audio and video."""
    # A list used for cleaning up
    delete: List[str] = []

    # For each url
    for url in urls:
        # Ignor url's if they start with #
        print("url: {}".format(url))
        if url[0] == "#":
            continue

        # Get the video stream
        yt = YouTube(url, on_complete_callback=complete)
        streams = yt.streams

        # Get video data
        title = yt.title
        title = slugify(title)
        src_path = path.join(music_path, "src")

        # Get video
        videotitle = title + "-video.mp4"
        videofile = path.join(src_path, videotitle)
        if path.exists(videofile):
            remove(videofile)
        stream = streams.get_highest_resolution()
        if stream is not None:
            stream.download(src_path, videotitle)
        else:
            print("Stream returned None.")
            continue

        # Get audio
        audiotitle = title + "-audio.mp4"
        audiofile = path.join(src_path, audiotitle)
        if path.exists(audiofile):
            remove(audiofile)
        stream = streams.get_audio_only()
        if stream is not None:
            stream.download(src_path, audiotitle)
        else:
            print("Stream returned None.")
            continue

        del stream

        # If the files should be combined
        if combine:
            file = path.join(music_path, title + ".mp4")
            combine_audio(videofile, audiofile, file)

            delete.append(videofile)
            delete.append(audiofile)

    # Delete the source files
    t = time()
    while len(delete) > 0:
        delete_copy = delete.copy()
        for file in delete_copy:
            try:
                remove(file)
                delete.remove(file)
            except PermissionError:
                pass
        if time() - t > 10:
            break


if __name__ == "__main__":
    # Get main directory
    main_path = getcwd()
    if main_path[-6:] != "loader":
        main_path = path.join(main_path, "musicdownloader")
        if not path.exists(main_path):
            raise FileNotFoundError("unable to locate main directory")

    # Setup file paths
    music_path = path.join(main_path, "music")
    rip_file = path.join(main_path, "rip.txt")
    if not path.exists(music_path):
        mkdir(music_path)
    if not path.exists(path.join(music_path, "src")):
        mkdir(path.join(music_path, "src"))
    if not path.exists(rip_file):
        rip = open(rip_file, "w")
        rip.close()

    # Run main
    main(get_urls(), True)
