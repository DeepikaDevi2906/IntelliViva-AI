import os
import whisper

# 🔥 Add ffmpeg path manually
os.environ["PATH"] += os.pathsep + r"C:\Users\devid\Downloads\ffmpeg-8.1-essentials_build\ffmpeg-8.1-essentials_build\bin"

model = whisper.load_model("base")

def convert_audio_to_text(audio_path):
    try:
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print("Whisper Error:", e)
        return "Error in transcription"