# preprocess_text.py

import spacy
import string
import nltk

# Only need to download once
nltk.download('punkt')

# Load spaCy model globally
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    doc = nlp(text)

    tokens = [token.text for token in doc]

    normalized = text.lower()
    normalized = ''.join(char for char in normalized if char not in string.punctuation)

    pos_tags = [(token.text, token.pos_) for token in doc]

    return {
        "original": text,
        "tokens": tokens,
        "normalized": normalized,
        "pos_tags": pos_tags
    }

# For testing directly:
if __name__ == "__main__":
    from audio_transcriber import transcribe_audio

    text = transcribe_audio("speech.wav")
    print("Transcribed:", text)

    processed = preprocess_text(text)

    print("\nTokens:", processed['tokens'])
    print("Normalized:", processed['normalized'])
    print("POS Tags:", processed['pos_tags'])
