from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Load Vennify grammar correction model
model_name = "vennify/t5-base-grammar-correction"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def correct_grammar(text):
    # Add grammar prefix for the model
    input_text = "grammar: " + text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        outputs = model.generate(
            inputs["input_ids"],
            max_length=256,
            num_beams=5,
            early_stopping=True
        )

    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_text

# Test directly
if __name__ == "__main__":
    while 1:
        sample_text = input()
        corrected = correct_grammar(sample_text)
        print("Original:", sample_text)
        print("Corrected:", corrected)
