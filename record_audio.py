import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
duration = 5  # Seconds of recording

print("🎤 Recording... Speak now!")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
write("speech.wav", fs, recording)  # Save as WAV file
print("✅ Recording complete and saved as speech.wav")
