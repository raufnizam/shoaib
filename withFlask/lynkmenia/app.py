from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__, static_folder='lynko/dist')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    mode = data.get('mode')

    # Process the URL and mode as needed
    
    print(f"URL: {url}, Mode: {mode}")
    
    # Dummy response
    return jsonify({"message": "Download started!", "url": url, "mode": mode})

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
