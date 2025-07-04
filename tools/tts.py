from gtts import gTTS
import os

def text_to_speech_arabic(text: str):
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")  # تأكد من تثبيت mpg123
