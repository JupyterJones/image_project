from os import listdir, path

def list_volk_videos(directory='static/vokoscreen_captures'):
    """
    Retrieves a sorted list of video files (with .mkv extension) in the given directory.
    """
    volk_directory = path.join(directory)
    return sorted(fn for fn in listdir(volk_directory) if fn.endswith('.mp4'))

def list_images(directory='static/images'):
    """
    Retrieves a sorted list of video files (with .mkv extension) in the given directory.
    """
    image_directory = path.join(directory)
    #return jpg png and jpeg
    image_list = sorted(fn for fn in listdir(image_directory) if fn.endswith('.jpg') or fn.endswith('.png') or fn.endswith('.jpeg'))
    return image_list    