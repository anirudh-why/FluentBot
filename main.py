from audio_transcriber import transcribe_audio
from preprocess_text import preprocess_text
from gec import correct_grammar

def main():
    audio_file = "speech.wav"
    # transcribed_text = transcribe_audio(audio_file)

    processed_text = preprocess_text(transcribed_text)
    print("\nPreprocessed Text:")
    print(f"Original: {processed_text['original']}")
    print(f"Tokens: {processed_text['tokens']}")
    print(f"Normalized: {processed_text['normalized']}")
    print(f"POS Tags: {processed_text['pos_tags']}")

    corrected_text = correct_grammar(transcribed_text)
    print("\nCorrected Text:")
    print(corrected_text)

if __name__ == "__main__":
    main()
