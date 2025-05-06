import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# Select a female English voice (if available)
for voice in voices:
    if "female" in voice.name.lower() and "english" in voice.languages[0].lower():
        engine.setProperty('voice', voice.id)
        break

# Set the speech rate (optional)
engine.setProperty('rate', 150)  # Adjust rate as per preference

# Set the volume (optional)
engine.setProperty('volume', 1.0)  # Volume range is 0.0 to 1.0

# Get the text to read from the CLI input
text_to_read = "He doesn't like talking to people who judge him, that's why he avoids them for a long time."

# Say the text
engine.say(text_to_read)

# Wait for the speech to finish
engine.runAndWait()

# Stop the engine after speaking
engine.stop()