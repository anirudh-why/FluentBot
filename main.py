from audio_transcriber import transcribe_audio
from preprocess_text import preprocess_text
from gec import correct_grammar
from text_to_speech import speakout
from record_audio import record
from datetime import datetime
import os


def grammerly():
    print("🎤 Press 'Enter' to start recording...")
    input()

    audio_file = "uploads/"+datetime.now().strftime("%Y%m%d%H%M%S") + "-speech.mp3"

    record(audio_file,8)

    transcribed_text = transcribe_audio(audio_file)

    # transcribed_text = "He don't likes talking to peoples who judges him that's why he avoid them since long time."

    processed_text = preprocess_text(transcribed_text)
    print("\nPreprocessed Text:")
    print(f"Original: {processed_text['original']}")
    print(f"Tokens: {processed_text['tokens']}")
    print(f"Normalized: {processed_text['normalized']}")
    print(f"POS Tags: {processed_text['pos_tags']}")

    corrected_text = correct_grammar(transcribed_text)
    print("\nCorrected Text:")
    print(corrected_text)

    speakout(corrected_text)

def main():
    in_dir = os.path.dirname(__file__) + "/uploads/"
    if not os.path.exists(in_dir):
        os.makedirs(in_dir)

    grammerly()


if __name__ == "__main__":
    main()
