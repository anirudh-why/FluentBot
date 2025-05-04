# audio_transcriber.py

import whisper
import warnings

# 🧼 Clean warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

print("📥 Loading Whisper model...")
model = whisper.load_model("base")  # You can try "small" or "medium" for better accuracy

def transcribe_audio(file_path):
    print(f"📝 Transcribing {file_path}...")
    result = model.transcribe(file_path)
    print("📃 Transcribed Text:")
    print(result["text"])
    return result["text"]

# Optional: run this file directly
if __name__ == "__main__":
    transcribe_audio("speech.wav")

    # 🧼 Clean up __pycache__
    import shutil
    import os
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
