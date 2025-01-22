from os import listdir, path

def list_volk_videos(directory='static/vokoscreen_captures'):
    """
    Retrieves a sorted list of video files (with .mkv extension) in the given directory.
    """
    volk_directory = path.join(directory)
    return sorted(fn for fn in listdir(volk_directory) if fn.endswith('.mp4'))