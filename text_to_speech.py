from gtts import gTTS
import os
from datetime import datetime


def speakout(text_to_read):
  # Use Google Text-to-Speech (gTTS)
  tts = gTTS(text=text_to_read, lang='en', slow=False)

  out_dir = os.path.dirname(__file__) + "/outputs/"
  if not os.path.exists(out_dir):
    os.makedirs(out_dir)

  file_path = out_dir + str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".mp3"

  # Save the speech to an audio file
  tts.save( file_path )

  # Play the audio file, I have vlc installed
  os.system("cvlc " + file_path)

  return file_path


if __name__ == "__main__":
  text_to_read = "He doesn't like talking to people who judge him, that's why he avoids them for a long time."
  speakout(text_to_read)