from flask import Flask, send_from_directory, request, jsonify, Response  # Ensure Response is imported
import subprocess
import json
import urllib.parse

app = Flask(__name__, static_folder='lynko/dist')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()  # This will correctly parse JSON data

    url = data.get('url')
    mode = data.get('mode')

    if not url or not mode:
        return jsonify({"error": "Missing 'url' or 'mode' in the form data"}), 400

    # Rest of the code...


    cookie_path = './www.youtube.com_cookies.txt'  # Path to your cookies file

    info_command = f"yt-dlp --cookies {cookie_path} --dump-json {url}"

    try:
        info_process = subprocess.Popen(info_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info_output, info_error = info_process.communicate()
        if info_process.returncode != 0:
            return jsonify({"error": info_error.decode()})

        video_info = json.loads(info_output)
        video_title = video_info.get('title', 'video')
        video_extension = video_info.get('ext', 'mp4')

        if mode == "video":
            command = f"yt-dlp --cookies {cookie_path} -o - {url} --add-header 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' --add-header 'Accept-Language:en-US,en;q=0.9'"
        elif mode == "audio":
            command = f"yt-dlp --cookies {cookie_path} --extract-audio --audio-format mp3 -o - {url}"
        elif mode == "playlist":
            command = f"yt-dlp --cookies {cookie_path} -i -o - {url}"
        else:
            return jsonify({"error": "Invalid mode specified. Use 'video', 'audio', or 'playlist'."})

        def generate():
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for chunk in iter(lambda: process.stdout.read(4096), b""):
                yield chunk
            process.stdout.close()

        filename = f"{video_title}.{video_extension}" if mode == "video" else f"{video_title}.mp3"
        safe_filename = urllib.parse.quote(filename)

        # Create the response object
        response = Response(generate(), content_type='application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{safe_filename}'

        return response

    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)})
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse video information."})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"})

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
