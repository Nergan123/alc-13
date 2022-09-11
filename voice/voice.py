import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from logger import LoggingHandler


class Voice(LoggingHandler):
    def __init__(self, lang):
        super().__init__()
        self.log.info(f'Language set to {lang}')
        self.lang = lang
        print('Setting voice')
        self.log.info(f'Setting voice')
        self.microphone = sr.Microphone()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        print('Voice set')
        self.log.info(f'Voice setup complete')

    def listen(self):
        try:
            with self.microphone as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                print('Listening...')
                self.log.info(f'Listening...')
                audio = self.recognizer.listen(mic)
                text_output = self.recognizer.recognize_google(audio)
                print(f'You said: {text_output}')
                self.log.info(f'User said: {text_output}')

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            text_output = '__Error__'
            self.log.error(sr.RequestError)

        except sr.UnknownValueError:
            print("Unknown error occurred")
            text_output = '__Error__'
            self.log.error(sr.UnknownValueError)

        return text_output

    def say(self, text_input):
        self.log.info(f'Alice: {text_input}')
        mp3_fp = BytesIO()
        tts = gTTS(text_input, lang=self.lang)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        speech = AudioSegment.from_file(mp3_fp, format="mp3")
        print(f'Alice: {text_input}')
        play(speech)
