from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Ensure download folder exists
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    # Get the YouTube URL from the frontend
    video_url = request.json.get('url')
    
    if not video_url:
        return jsonify({'status': 'failed', 'message': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'extractaudio': True,  # Extract audio (can be turned off if you want video too)
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
            'nocheckcertificate': True,  # Disable SSL certificate validation
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract information and download the video
            info_dict = ydl.extract_info(video_url, download=True)
            video_url = info_dict.get('url', None)

            if video_url:
                return jsonify({'status': 'success', 'video_url': video_url}), 200
            else:
                return jsonify({'status': 'failed', 'message': 'Could not extract video URL'}), 400

    except Exception as e:
        return jsonify({'status': 'failed', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
