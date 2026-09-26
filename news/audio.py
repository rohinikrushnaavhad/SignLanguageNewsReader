
from gtts import gTTS

def create_audio(text, output_path):
    tts = gTTS(text=text, lang="en")
    tts.save(output_path)
    return output_path
