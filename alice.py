from voice.voice import Voice
from processing.nlp_model import Language_processing
from voice.chat_module import Chat_module
import os


class Alice:
    def __init__(self, lang):
        self.voice = Voice(lang)
        self.processor = Language_processing()
        self.chat = Chat_module()
        if (
                (not os.path.exists('ai_storage/alice_v1.h5')) or
                len(os.listdir('ai_storage/weights/')) == 0
        ):
            print('model does not exist')
            self.processor.create_dataset()
            self.processor.build_and_train_model()

        self.processor.load_model()
        self.state = 'Action_based'

    def run(self):
        while True:
            if self.state == 'Action_based':
                phrase = self.voice.listen()
                intents = self.processor.pred_class(phrase)
                response = self.processor.get_response(intents)
                self.voice.say(response)
                print(f'Alice: {response}')
                if intents[0] == "chat":
                    phrase = self.voice.listen()
                    if "yes" in phrase or "yeah" in phrase:
                        self.state = "Chat_mode"
                if 'goodbye' in intents:
                    break
            elif self.state == 'Chat_mode':
                phrase = self.voice.listen()
                intents = self.processor.pred_class(phrase)
                if intents[0] == 'end_chat':
                    response = self.processor.get_response(intents)
                    self.state = 'Action_based'
                else:
                    response = self.chat.get_response(phrase)
                print(f'Alice: {response}')
                self.voice.say(response)
