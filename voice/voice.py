import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play


class Voice:
    def __init__(self, lang):
        self.lang = lang
        print('Setting voice')
        self.microphone = sr.Microphone()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        print('Voice set')

    def listen(self):
        try:
            with self.microphone as mic:
                print('Listening...')
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                audio = self.recognizer.listen(mic)
                text_output = self.recognizer.recognize_google(audio)
                print(f'You said: {text_output}')

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            text_output = 'Error'

        except sr.UnknownValueError:
            print("Unknown error occurred")
            text_output = 'Error'

        return text_output

    def say(self, text_input):
        mp3_fp = BytesIO()
        tts = gTTS(text_input, lang=self.lang)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        speech = AudioSegment.from_file(mp3_fp, format="mp3")
        play(speech)
