from voice.voice import Voice
from processing.nlp_model import Language_processing


class Alice:
    def __init__(self, lang):
        self.voice = Voice(lang)
        self.processor = Language_processing()
        self.processor.create_dataset()
        self.processor.build_and_train_model()
        self.processor.load_model()
        self.state = 'Action_based'

    def start(self):
        while True:
            if self.state == 'Action_based':
                phrase = self.voice.listen()
                intents = self.processor.pred_class(phrase)
                response = self.processor.get_response(intents)
                self.voice.say(response)
                if 'goodbye' in intents:
                    break
