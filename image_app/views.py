from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from moviepy.editor import VideoFileClip
import os
import subprocess
from icecream import ic
from .utilities import list_volk_videos, list_images
import shutil
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
    file_path = os.path.join('static', 'TEXT/ALL.txt')
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
        # Extract POST data
        video_name = request.POST.get("video_name")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        crop_width = request.POST.get("crop_width", "940")
        crop_height = request.POST.get("crop_height", "540")
        crop_x = request.POST.get("crop_x", "300")
        crop_y = request.POST.get("crop_y", "400")

        # Validate required input
        if not video_name or not start_time or not end_time:
            ic("Missing required fields!")
            return redirect(f'/edit-video/?video_name={video_name}&error=Missing required fields.')

        # Convert start and end times to float
        try:
            start_time = float(start_time)
            end_time = float(end_time)
        except ValueError:
            ic("Invalid time values!")
            return redirect(f'/edit-video/?video_name={video_name}&error=Invalid time values.')

        # Paths
        input_path = os.path.join(settings.STATICFILES_DIRS[0], 'vokoscreen_captures', video_name)
        output_dir = os.path.join(settings.STATICFILES_DIRS[0], 'trimmed_videos')
        os.makedirs(output_dir, exist_ok=True)

        # Check if the input file exists
        if not os.path.exists(input_path):
            ic(f"Input file does not exist: {input_path}")
            return redirect(f'/edit-video/?video_name={video_name}&error=Input file not found.')

        # FFmpeg processing
        output_path = os.path.join(output_dir, f"ffmpeg_trimmed_{video_name}")
        overlay_path = os.path.join(settings.STATICFILES_DIRS[0], 'assets', 'django_frame.png')
        ffmpeg_command = [
            "ffmpeg",
            "-ss", str(start_time),
            "-i", input_path,
            "-i", overlay_path,
            "-filter_complex", f"[0:v]crop={crop_width}:{crop_height}:{crop_x}:{crop_y},scale=1366x768,unsharp=5:5:1.0[v];[v][1:v]overlay=0:0",
            "-t", str(end_time - start_time),
            "-y",
            output_path
        ]

        try:
            # Run FFmpeg command
            subprocess.run(ffmpeg_command, check=True)
            # copy the output file to the static/vokoscreen_captures folder
            shutil.copy(output_path, os.path.join(settings.STATICFILES_DIRS[0], 'vokoscreen_captures'))
            ic(f"FFmpeg processed video saved at: {output_path}")
            return render(request, 'trimmed_video.html', {'video_name': f"ffmpeg_trimmed_{video_name}"})
        except subprocess.CalledProcessError as e:
            ic(f"FFmpeg processing failed: {e}")
            return redirect(f'/edit-video/?video_name={video_name}&error=FFmpeg processing failed.')

        # MoviePy fallback (optional)
        try:
            output_path = os.path.join(output_dir, f"moviepy_trimmed_{video_name}")
            with VideoFileClip(input_path) as video:
                trimmed_video = video.subclip(start_time, end_time)
                trimmed_video.write_videofile(output_path, codec="libx264")
            ic(f"MoviePy processed video saved at: {output_path}")
            return render(request, 'trimmed_video.html', {'video_name': f"moviepy_trimmed_{video_name}"})
        except Exception as e:
            ic(f"MoviePy processing failed: {e}")
            return redirect(f'/edit-video/?video_name={video_name}&error=MoviePy processing failed.')

    # If request.method is not POST, redirect to the video list
    return redirect('/show-videos/')

# View to render the trim video form
def trim_video(request):
    if request.method == "POST":
        # Extract video name from POST data
        video_name = request.POST.get("video_name")
        ic(f"Received video_name: {video_name}")

        # If video_name is empty, handle the case
        if not video_name:
            ic("No video name provided!")
            return render(request, 'trim_video.html', {'error': "Video name is required."})

        # Redirect to the same page with the video name as a query parameter
        return redirect(f'/trim-video/?video={video_name}')

    # Handle GET request
    video_name = request.GET.get('video')  # Extract video name from query parameter
    ic(f"Rendering video: {video_name}")

    if not video_name:
        # Handle case where video is not provided
        return render(request, 'trim_video.html', {'error': "No video selected to play."})

    # Render template with the video name
    return render(request, 'trim_video.html', {'video': video_name})


def trim_only(request):
    if request.method == "POST":
        # Extract POST data
        video_name = request.POST.get("video_name")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        # Validate input
        if not video_name or not start_time or not end_time:
            return render(request, 'trim_video.html', {
                'error': "Missing required fields.",
                'video': video_name,
            })
        
        try:
            # Convert start and end times to float
            start_time = float(start_time)
            end_time = float(end_time)

            # Validate timing
            if start_time >= end_time:
                return render(request, 'trim_video.html', {
                    'error': "End time must be greater than start time.",
                    'video': video_name,
                })
            
            # Paths for video input and output
            input_path = f'static/vokoscreen_captures/{video_name}'
            output_path = f'static/vokoscreen_captures/trimmed_{video_name}'

            # Trim the video using moviepy
            with VideoFileClip(input_path) as video:
                trimmed_clip = video.subclip(start_time, end_time)
                trimmed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            # Pass the trimmed video back to the user
            return render(request, 'trim_video.html', {
                'success': "Video trimmed successfully!",
                'video': f'trimmed_{video_name}',
            })
        
        except Exception as e:
            return render(request, 'trim_video.html', {
                'error': f"An error occurred: {str(e)}",
                'video': video_name,
            })
    
    # Handle GET request or invalid method
    return render(request, 'trim_video.html', {'error': "Invalid request method."})

def delete_video(request, video_name):
    if request.method == "POST":
        # Construct the correct file path for the video
        video_path = os.path.join(settings.BASE_DIR, 'static', 'vokoscreen_captures', video_name)

        # Debug: Log the video path for troubleshooting
        print(f"Attempting to delete video at: {video_path}")

        # Check if the file exists before attempting to delete it
        if os.path.exists(video_path):
            try:
                os.remove(video_path)
                # Redirect back to the video list with a success message
                return redirect('show_videos')
            except Exception as e:
                # Redirect with an error message if deletion fails
                return redirect('show_videos', error=f"Error deleting video: {str(e)}")
        else:
            # Redirect with an error message if the file doesn't exist
            return redirect('show_videos', error="Video file not found.")
    # Redirect with a general error if method is not POST
    return redirect('show_videos', error="Invalid request method.")
