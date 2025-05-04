# gec.py

from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Load pre-trained model and tokenizer
model_name = "prithivida/grammar_error_correcter_v1"  # Pre-trained GEC model on HuggingFace
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def correct_grammar(text):
    # Tokenize the input text
    input_text = "grammar error correction: " + text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    
    # Generate the corrected sentence
    with torch.no_grad():
        output = model.generate(inputs["input_ids"], num_beams=5, max_length=256, early_stopping=True)
    
    # Decode and return corrected text
    corrected_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return corrected_text

# For testing directly
if __name__ == "__main__":
    incorrect_text = "She go to school every day."
    corrected = correct_grammar(incorrect_text)
    print(f"Original Text: {incorrect_text}")
    print(f"Corrected Text: {corrected}")
