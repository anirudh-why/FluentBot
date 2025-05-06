import os
from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from datetime import datetime

from audio_transcriber import transcribe_audio
from preprocess_text import preprocess_text
from gec import correct_grammar
from text_to_speech import speakout

app = FastAPI()

# Make sure the 'uploads' directory exists
uploads_dir = Path("uploads")
uploads_dir.mkdir(parents=True, exist_ok=True)

@app.post("/correct/")
async def create_upload_file(audio: UploadFile = File(...)):
    # Define the file path
    file_location = uploads_dir / str(datetime.now().strftime("%Y%m%d%H%M%S") + "_"+audio.filename)
    
    # Save the file
    with open(file_location, "wb") as buffer:
        # Read the file in chunks and write it to the destination file
        while chunk := await audio.read(1024):  # You can adjust the chunk size
            buffer.write(chunk)

    audio_file = "speech.wav"
    transcribed_text = transcribe_audio(file_location)

    processed_text = preprocess_text(transcribed_text)
    print("\nPreprocessed Text:")
    print(f"Original: {processed_text['original']}")
    print(f"Tokens: {processed_text['tokens']}")
    print(f"Normalized: {processed_text['normalized']}")
    print(f"POS Tags: {processed_text['pos_tags']}")

    corrected_text = correct_grammar(transcribed_text)
    print("\nCorrected Text:")
    print(corrected_text)

    op_path=speakout(corrected_text)
    
    return {"filename": audio.filename, "path": str(op_path)}
