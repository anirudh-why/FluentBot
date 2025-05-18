import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
from datetime import datetime
import speech_recognition as sr
from gtts import gTTS
import shutil
from pydub import AudioSegment
import tempfile

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Make sure the directories exist
uploads_dir = Path("uploads")
outputs_dir = Path("outputs")
uploads_dir.mkdir(parents=True, exist_ok=True)
outputs_dir.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="outputs"), name="static")

def convert_to_wav(input_path, output_path):
    """Convert audio file to WAV format"""
    try:
        # Load the audio file
        audio = AudioSegment.from_file(str(input_path))
        # Export as WAV
        audio.export(str(output_path), format="wav")
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error converting audio format: {str(e)}")

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    current_time = datetime.now()
    for directory in [uploads_dir, outputs_dir]:
        for file in directory.glob("*"):
            if (current_time - datetime.fromtimestamp(file.stat().st_mtime)).total_seconds() > 3600:
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Error deleting file {file}: {e}")

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(str(audio_path)) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                raise HTTPException(status_code=400, detail="Could not understand audio")
            except sr.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Error with speech recognition service: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio file: {str(e)}")

def correct_grammar(text):
    if not text:
        return ""
        
    # Simple grammar correction (you can replace this with a more sophisticated model)
    corrections = {
        "i": "I",
        "im": "I'm",
        "dont": "don't",
        "cant": "can't",
        "wont": "won't",
        "its": "it's",
        "thats": "that's",
        "youre": "you're",
        "theyre": "they're",
        "were": "we're",
        "hes": "he's",
        "shes": "she's"
    }
    
    words = text.split()
    corrected_words = [corrections.get(word.lower(), word) for word in words]
    return " ".join(corrected_words)

def text_to_speech(text, output_path):
    if not text:
        return None
        
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(str(output_path))
        return output_path.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in text-to-speech: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to Grammar Correction API"}

@app.post("/correct/")
async def create_upload_file(audio: UploadFile = File(...)):
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    if not audio.filename.lower().endswith(('.wav', '.mp3', '.ogg', '.webm')):
        raise HTTPException(status_code=400, detail="Only audio files are allowed")

    try:
        # Clean up old files
        cleanup_old_files()
        
        # Define the file paths
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        temp_input_path = uploads_dir / f"{timestamp}_input_{audio.filename}"
        wav_path = uploads_dir / f"{timestamp}_converted.wav"
        output_path = outputs_dir / f"{timestamp}_corrected.mp3"
        
        # Save the uploaded file
        with open(temp_input_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)

        # Convert to WAV format
        convert_to_wav(temp_input_path, wav_path)

        # Process the audio
        transcribed_text = transcribe_audio(wav_path)
        corrected_text = correct_grammar(transcribed_text)
        
        # Generate audio for corrected text
        audio_filename = text_to_speech(corrected_text, output_path)
        
        # Clean up temporary files
        try:
            temp_input_path.unlink()
            wav_path.unlink()
        except Exception as e:
            print(f"Error deleting temporary files: {e}")
        
        return {
            "original_text": transcribed_text,
            "corrected_text": corrected_text,
            "audio_path": audio_filename
        }
        
    except HTTPException as he:
        # Clean up files in case of error
        try:
            if temp_input_path.exists():
                temp_input_path.unlink()
            if wav_path.exists():
                wav_path.unlink()
            if output_path.exists():
                output_path.unlink()
        except Exception as e:
            print(f"Error cleaning up files: {e}")
        raise he
    except Exception as e:
        # Clean up files in case of error
        try:
            if temp_input_path.exists():
                temp_input_path.unlink()
            if wav_path.exists():
                wav_path.unlink()
            if output_path.exists():
                output_path.unlink()
        except Exception as cleanup_error:
            print(f"Error cleaning up files: {cleanup_error}")
        raise HTTPException(status_code=500, detail=str(e))
