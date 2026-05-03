from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from services.speech_to_text import convert_audio_to_text

import subprocess
audio_bp = Blueprint("audio", __name__)

# Allowed file types
ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a", "aac", "webm", "ogg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



@audio_bp.route("/upload-audio", methods=["POST"])
def upload_audio():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file key"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Unsupported file format"}), 400

        upload_folder = os.path.join(os.getcwd(), "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        import time
        filename = f"{int(time.time())}_{secure_filename(file.filename)}"

        input_path = os.path.join(upload_folder, filename)
        file.save(input_path)

        # 🔥 Convert to WAV
        output_path = input_path.rsplit(".", 1)[0] + ".wav"

        subprocess.run([
            "ffmpeg", "-i", input_path, output_path
        ])

        return jsonify({
            "message": "Success",
            "transcript": text
        })

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500