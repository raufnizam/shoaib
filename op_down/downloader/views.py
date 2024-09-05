import subprocess
import json
import urllib.parse
import os
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Render the index page with two separate forms (YouTube and other platforms)
def index(request):
    HERO_CONTENT = "All Video Downloader is a versatile software application designed to help users download videos from a wide range of online platforms, including popular sites like YouTube, Vimeo, Facebook, Instagram, and more."
    
    ABOUT_TEXT = "Discover the perfect tool for fast and efficient video and music downloads from the web: our All video downloader. This intuitive, free application simplifies the process of securing your favorite media content with just one click, ensuring a smooth and hassle-free experience!"
    
    CONTACT = {
        "phoneNo": "+12 4555 666 00",
        "email": "me@example.com"
    }

    context = {
        "HERO_CONTENT": HERO_CONTENT,
        "ABOUT_TEXT": ABOUT_TEXT,
        "CONTACT": CONTACT,
    }
    return render(request, 'downloader/index.html', context)


@csrf_exempt  # Handle CSRF tokens correctly
def send_cookies(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        browser_cookies = data.get('cookies', '')
        # Write the cookies to a file for yt-dlp to use
        cookie_path = './cookies.txt'
        with open(cookie_path, 'w') as cookie_file:
            # Format cookies to Netscape format or the format yt-dlp expects
            cookie_file.write('# Netscape HTTP Cookie File\n')
            for cookie in browser_cookies.split(';'):
                key, value = cookie.strip().split('=', 1)
                cookie_file.write(f'.youtube.com\tTRUE\t/\tFALSE\t0\t{key}\t{value}\n')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)


# Download function to handle different platforms
def download(request):
    url = request.POST.get('url')
    mode = request.POST.get('mode')
    platform = request.POST.get('platform')
    cookie_path = './cookies.txt'
    
    # Check if YouTube form was submitted
    if platform == 'youtube':
        if not os.path.isfile(cookie_path):
            return JsonResponse({"error": "Cookies file does not exist or is not readable."})

        info_command = f"yt-dlp --cookies {cookie_path} --dump-json {url}"

        try:
            info_process = subprocess.Popen(info_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            info_output, info_error = info_process.communicate()

            if info_process.returncode != 0:
                return JsonResponse({"error": info_error.decode()})

            video_info = json.loads(info_output)
            video_title = video_info.get('title', 'video')
            video_extension = video_info.get('ext', 'mp4')

            if mode == "video":
                command = f"yt-dlp --cookies {cookie_path} -o - {url} --add-header 'User-Agent:Mozilla/5.0'"
            elif mode == "audio":
                command = f"yt-dlp --cookies {cookie_path} --extract-audio --audio-format mp3 -o - {url}"
            elif mode == "playlist":
                command = f"yt-dlp --cookies {cookie_path} -i -o - {url}"
            else:
                return JsonResponse({"error": "Invalid mode specified. Use 'video', 'audio', or 'playlist'."})

            return execute_download(command, video_title, video_extension, mode)

        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Failed to parse video information."})
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"})

    # Handle other platforms (not YouTube)
    else:
        if mode == "video":
            command = f"yt-dlp -o - {url} --add-header 'User-Agent:Mozilla/5.0'"
        elif mode == "audio":
            command = f"yt-dlp --extract-audio --audio-format mp3 -o - {url}"
        elif mode == "playlist":
            command = f"yt-dlp -i -o - {url}"
        else:
            return JsonResponse({"error": "Invalid mode specified. Use 'video', 'audio', or 'playlist'."})

        try:
            info_command = f"yt-dlp --dump-json {url}"
            info_process = subprocess.Popen(info_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            info_output, info_error = info_process.communicate()

            if info_process.returncode != 0:
                return JsonResponse({"error": info_error.decode()})

            video_info = json.loads(info_output)
            video_title = video_info.get('title', 'video')
            video_extension = video_info.get('ext', 'mp4')

            return execute_download(command, video_title, video_extension, mode)

        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Failed to parse video information."})
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"})


# Helper function to handle file download generation
def execute_download(command, video_title, video_extension, mode):
    def generate():
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for chunk in iter(lambda: process.stdout.read(4096), b""):
            yield chunk
        process.stdout.close()

    filename = f"{video_title}.{video_extension}" if mode == "video" else f"{video_title}.mp3"
    safe_filename = urllib.parse.quote(filename)

    response = StreamingHttpResponse(generate(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{safe_filename}'
    return response
