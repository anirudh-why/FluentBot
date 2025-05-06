import sounddevice as sd
from scipy.io.wavfile import write


fs = 44100  # Sample rate


def record(file_name="speech.wav", duration=5):
  print("🎤 Recording... Speak now!")
  recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
  sd.wait()  # Wait until recording is finished
  write(file_name, fs, recording)  # Save as WAV file
  print("✅ Recording complete and saved as ", file_name)


if __name__ == "__main__":
  record()