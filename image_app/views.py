from django.shortcuts import render
import os
# Create your views here.
from os import listdir, path
from django.conf import settings

from .utilities import list_volk_videos
from .utilities import list_images

def show_videos(request):
    videos = list_volk_videos()
    return render(request, 'show_videos.html', {'videos': videos})

def show_image(request):
    images = list_images()
    return render(request, 'show_image.html', {'images': images})

def show_text(request):
    # Specify the path to the text file
    file_path = os.path.join('static', 'session.txt')
    
    # Read the file content
    with open(file_path, 'r') as file:
        text_content = file.read()

    # Pass the text content to the template
    return render(request, 'show_text.html', {'text_content': text_content})

def search_code(request):
    # Specify the path to the text file
    file_path = os.path.join('static', 'TEXT/chat1_2.txt')
    
    # Read the file content
    with open(file_path, 'r') as file:
        text_content = file.read()

    # Pass the text content to the template
    return render(request, 'search_code.html', {'text_content': text_content})
    
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

# Directory to store text files
TEXT_DIR = os.path.join(settings.BASE_DIR, 'static', 'TEXT')
if not os.path.exists(TEXT_DIR):
    os.makedirs(TEXT_DIR)  # Ensure the directory exists

def edit_text(request):
    selected_file = None
    content = ''

    if request.method == 'POST':
        # Get filename and content from the request
        filename = request.POST.get('filename', '').strip()
        content = request.POST.get('content', '')

        if filename:
            # Ensure filename ends with .txt
            if not filename.endswith('.txt'):
                filename += '.txt'

            # Save the file in TEXT_DIR
            file_path = os.path.join(TEXT_DIR, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            selected_file = filename  # Keep track of the file being edited
        else:
            error_message = "Filename is required!"
            return render(request, 'edit_text.html', {
                'files': _get_files_in_directory(),
                'selected_file': selected_file,
                'content': content,
                'error_message': error_message,
            })

    elif request.method == 'GET':
        # Handle file selection from the GET request
        selected_file = request.GET.get('file', '')
        if selected_file:
            file_path = os.path.join(TEXT_DIR, selected_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

    # Render the page with files and content
    return render(request, 'edit_text.html', {
        'files': _get_files_in_directory(),
        'selected_file': selected_file,
        'content': content,
    })

def _get_files_in_directory():
    """Helper function to list all text files in the TEXT_DIR."""
    return [f for f in os.listdir(TEXT_DIR) if f.endswith('.txt')]     