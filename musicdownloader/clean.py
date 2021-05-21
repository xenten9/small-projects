from os import getcwd, path, remove, listdir

main_path = getcwd()
if main_path[-6:] != 'loader':
    main_path = path.join(main_path, 'music downloader')
    if not path.exists(main_path):
        raise FileNotFoundError('unable to locate main directory')
music_path = path.join(main_path, 'music')
src_path = path.join(music_path, 'src')

for file in listdir(src_path):
    if file.endswith('.mp4'):
        try:
            remove(path.join(src_path, file))
        except PermissionError:
            pass
