import subprocess
import json
import urllib.parse
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render

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

def download(request):
    url = request.POST.get('url')
    mode = request.POST.get('mode')

    # Convert cookies from the request to a cookie header string
    cookies = request.COOKIES
    cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])
    print(cookie_header)

    info_command = f"yt-dlp --add-header 'Cookie:{cookie_header}' --dump-json {url}"

    try:
        info_process = subprocess.Popen(info_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info_output, info_error = info_process.communicate()

        if info_process.returncode != 0:
            return JsonResponse({"error": info_error.decode()})

        video_info = json.loads(info_output)
        video_title = video_info.get('title', 'video')
        video_extension = video_info.get('ext', 'mp4')

        if mode == "video":
            command = f"yt-dlp --add-header 'Cookie:{cookie_header}' -o - {url} --add-header 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' --add-header 'Accept-Language:en-US,en;q=0.9'"
        elif mode == "audio":
            command = f"yt-dlp --add-header 'Cookie:{cookie_header}' --extract-audio --audio-format mp3 -o - {url}"
        elif mode == "playlist":
            command = f"yt-dlp --add-header 'Cookie:{cookie_header}' -i -o - {url}"
        else:
            return JsonResponse({"error": "Invalid mode specified. Use 'video', 'audio', or 'playlist'."})

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

    except subprocess.CalledProcessError as e:
        return JsonResponse({"error": str(e)})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Failed to parse video information."})
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"})
