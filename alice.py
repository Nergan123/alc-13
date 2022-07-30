from voice.voice import Voice
from processing.speech_processing import Speech_processor


class Alice:
    def __init__(self, lang):
        self.voice = Voice(lang)
        self.processor = Speech_processor()

    def start(self):
        while True:
            phrase = self.voice.listen()
            action = self.processor.choose_action(phrase)
            response = self.processor.generate_response(action)
            self.voice.say(response)
            if action == 'farewell':
                break
