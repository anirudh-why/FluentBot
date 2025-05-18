import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import re

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def check_grammar(text):
    # Tokenize and tag parts of speech
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    
    corrections = []
    corrected_text = text
    
    # Check for common grammar mistakes
    # 1. Subject-verb agreement
    for i, (word, tag) in enumerate(pos_tags):
        if i > 0 and tag.startswith('VB') and pos_tags[i-1][1] == 'PRP':
            if pos_tags[i-1][0].lower() in ['he', 'she', 'it'] and word.endswith('s'):
                continue
            elif pos_tags[i-1][0].lower() in ['i', 'you', 'we', 'they'] and not word.endswith('s'):
                continue
            else:
                if pos_tags[i-1][0].lower() in ['he', 'she', 'it']:
                    if not word.endswith('s'):
                        corrected_word = word + 's'
                        corrections.append(f"Subject-verb agreement: Changed '{word}' to '{corrected_word}'")
                        corrected_text = corrected_text.replace(word, corrected_word)
                else:
                    if word.endswith('s'):
                        corrected_word = word[:-1]
                        corrections.append(f"Subject-verb agreement: Changed '{word}' to '{corrected_word}'")
                        corrected_text = corrected_text.replace(word, corrected_word)
    
    # 2. Check for common contractions
    contractions = {
        "dont": "don't",
        "cant": "can't",
        "wont": "won't",
        "shouldnt": "shouldn't",
        "couldnt": "couldn't",
        "wouldnt": "wouldn't",
        "isnt": "isn't",
        "arent": "aren't",
        "wasnt": "wasn't",
        "werent": "weren't"
    }
    
    for wrong, correct in contractions.items():
        if wrong in text.lower():
            corrections.append(f"Contraction: Changed '{wrong}' to '{correct}'")
            corrected_text = re.sub(r'\b' + wrong + r'\b', correct, corrected_text, flags=re.IGNORECASE)
    
    # 3. Check for capitalization at the beginning of sentences
    sentences = nltk.sent_tokenize(corrected_text)
    corrected_sentences = []
    for sentence in sentences:
        if sentence and not sentence[0].isupper():
            corrected_sentences.append(sentence[0].upper() + sentence[1:])
            corrections.append(f"Capitalization: Capitalized first letter of sentence")
        else:
            corrected_sentences.append(sentence)
    corrected_text = ' '.join(corrected_sentences)
    
    return {
        "corrected_text": corrected_text,
        "corrections": corrections
    } 