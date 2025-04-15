from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is working!"

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided."}), 400

    try:
        unique_id = str(uuid.uuid4())
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{unique_id}.%(ext)s',
            'cookiefile': 'cookies.txt',  # Use exported YouTube cookies
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info)

        response = send_file(file_name, as_attachment=True)

        @response.call_on_close
        def cleanup():
            try:
                os.remove(file_name)
            except Exception as e:
                print(f"Cleanup error: {e}")

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
