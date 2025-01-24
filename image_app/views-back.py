from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from moviepy.editor import VideoFileClip
import os
import subprocess
from icecream import ic
from .utilities import list_volk_videos, list_images

# Directory to store text files
TEXT_DIR = os.path.join(settings.BASE_DIR, 'static', 'TEXT')
if not os.path.exists(TEXT_DIR):
    os.makedirs(TEXT_DIR)  # Ensure the directory exists


# View to display videos
def show_videos(request):
    videos = list_volk_videos()
    return render(request, 'show_videos.html', {'videos': videos})


# View to display images
def show_image(request):
    images = list_images()
    return render(request, 'show_image.html', {'images': images})


# View to display text from a file
def show_text(request):
    file_path = os.path.join('static', 'session.txt')
    with open(file_path, 'r') as file:
        text_content = file.read()
    return render(request, 'show_text.html', {'text_content': text_content})


# View to display code from a specific file
def search_code(request):
    file_path = os.path.join('static', 'TEXT/chat1_2.txt')
    with open(file_path, 'r') as file:
        text_content = file.read()
    return render(request, 'search_code.html', {'text_content': text_content})


# View to display Jonna's text file
def show_jonna(request):
    file_path = os.path.join('static', 'Sankalp_Jonna.txt')
    with open(file_path, 'r') as file:
        text_content = file.read()
    return render(request, 'show_text.html', {'text_content': text_content})


# View for the homepage
def index(request):
    return render(request, 'index.html')


# Helper function to list all text files in TEXT_DIR
def _get_files_in_directory():
    return [f for f in os.listdir(TEXT_DIR) if f.endswith('.txt')]


# View to edit text files
def edit_text(request):
    selected_file = None
    content = ''

    if request.method == 'POST':
        filename = request.POST.get('filename', '').strip()
        content = request.POST.get('content', '')

        if filename:
            if not filename.endswith('.txt'):
                filename += '.txt'
            file_path = os.path.join(TEXT_DIR, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            selected_file = filename
        else:
            return render(request, 'edit_text.html', {
                'files': _get_files_in_directory(),
                'selected_file': selected_file,
                'content': content,
                'error_message': "Filename is required!",
            })

    elif request.method == 'GET':
        selected_file = request.GET.get('file', '')
        if selected_file:
            file_path = os.path.join(TEXT_DIR, selected_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

    return render(request, 'edit_text.html', {
        'files': _get_files_in_directory(),
        'selected_file': selected_file,
        'content': content,
    })


# View to render the video editing page
def edit_video(request, video_name=None):
    if video_name:
        video_path = os.path.join(settings.STATICFILES_DIRS[0], 'vokoscreen_captures', video_name)
        if os.path.exists(video_path):
            return render(request, 'edit_video.html', {'video_name': video_name})
        else:
            return render(request, 'edit_video.html', {'error': "Video not found."})
    return render(request, 'edit_video.html', {'error': "No video selected."})


# View to trim videos
@csrf_exempt
def process_trim(request):
    if request.method == "POST":
        # Get the video_name from the form data
        video_name = request.POST.get('video_name')
        ic(video_name)
        if not video_name:
            # If no video was selected, show an error
            return render(request, 'trim_video.html', {
                'error_message': 'No video selected for editing.'
            })

        # If video_name is found, proceed to trimming logic
        # Assuming you have a trimming process here (replace with actual logic)
        return render(request, 'trim_video.html', {
            'video_name': video_name
        })
    else:
        # For non-POST requests, render an error or redirect
        return render(request, 'trim_video.html', {'error': 'Invalid request method.'})

# View to render the trim video form
def trim_video(request):
    if request.method == "GET":
        return render(request, 'trim_video.html')
    return render(request, 'trim_video.html', {'error': "Invalid request method."})
