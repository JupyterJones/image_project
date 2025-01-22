from django.shortcuts import render
import os
# Create your views here.
from os import listdir, path

from .utilities import list_volk_videos

def show_videos(request):
    videos = list_volk_videos()
    return render(request, 'show_videos.html', {'videos': videos})

def show_image(request):
    return render(request, 'show_image.html')

def show_text(request):
    # Specify the path to the text file
    file_path = os.path.join('static', 'session.txt')
    
    # Read the file content
    with open(file_path, 'r') as file:
        text_content = file.read()

    # Pass the text content to the template
    return render(request, 'show_text.html', {'text_content': text_content})
def show_jonna(request):
    # Specify the path to the text file
    file_path = os.path.join('static', 'Sankalp_Jonna.txt')
    
    # Read the file content
    with open(file_path, 'r') as file:
        text_content = file.read()

    # Pass the text content to the template
    return render(request, 'show_text.html', {'text_content': text_content})
def index(request):
    return render(request, 'index.html')   