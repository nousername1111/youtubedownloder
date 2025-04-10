from flask import Flask, request, send_file
import yt_dlp
import tempfile
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    fmt = data['format']
    temp_dir = tempfile.mkdtemp()

    if fmt == 'mp3':
        options = {
            'format': 'bestaudio',
            'outtmpl': f'{temp_dir}/audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
    elif fmt == '360':
        options = {
            'format': '18',
            'outtmpl': f'{temp_dir}/video.mp4',
        }
    elif fmt == '720':
        options = {
            'format': '22',
            'outtmpl': f'{temp_dir}/video.mp4',
        }
    else:
        options = {
            'format': 'best',
            'outtmpl': f'{temp_dir}/video.%(ext)s',
        }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        if fmt == 'mp3':
            file_path = file_path.rsplit('.', 1)[0] + '.mp3'

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
