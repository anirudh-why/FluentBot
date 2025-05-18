from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import speech_recognition as sr
from pydub import AudioSegment
import io
import tempfile
import os
from datetime import datetime
from audio_transcriber import transcribe_audio
from preprocess_text import preprocess_text
from gec import correct_grammar
from text_to_speech import speakout
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Mount the uploads directory to serve static files
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

@app.post("/process-audio")
async def process_audio(audio: UploadFile = File(...)):
    logger.info(f"Received audio file: {audio.filename}")
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    audio_file = f"{UPLOADS_DIR}/{timestamp}-speech.mp3"
    
    # Save the uploaded file
    with open(audio_file, "wb") as buffer:
        content = await audio.read()
        buffer.write(content)
    logger.info(f"Saved audio file to: {audio_file}")

    try:
        # Transcribe audio
        logger.info("Starting audio transcription...")
        transcribed_text = transcribe_audio(audio_file)
        logger.info(f"Transcribed text: {transcribed_text}")
        
        # Preprocess text
        logger.info("Preprocessing text...")
        processed_text = preprocess_text(transcribed_text)
        logger.info(f"Preprocessed text: {processed_text}")
        
        # Correct grammar
        logger.info("Correcting grammar...")
        corrected_text = correct_grammar(transcribed_text)
        logger.info(f"Corrected text: {corrected_text}")
        
        # Generate audio for corrected text
        audio_path = f"{UPLOADS_DIR}/{timestamp}-corrected.mp3"
        logger.info("Generating corrected audio...")
        speakout(corrected_text, audio_path)
        logger.info(f"Generated audio file: {audio_path}")

        return {
            "original_text": transcribed_text,
            "corrected_text": corrected_text,
            "corrections": processed_text.get("corrections", []),
            "audio_path": audio_path,
            "processing_details": {
                "transcription": transcribed_text,
                "preprocessing": processed_text,
                "correction": corrected_text
            }
        }

    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        return {"error": str(e)}

    finally:
        # Clean up the original audio file
        if os.path.exists(audio_file):
            os.unlink(audio_file)
            logger.info(f"Cleaned up temporary file: {audio_file}")

@app.get("/")
async def read_root():
    return {"message": "Grammar Correction API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
