from voice.voice import Voice
from voice.chat_module import Chat_module
from processing.weather import Weather_module
from processing.phrase_analysis import Phrase_analysis
import os
from dotenv import load_dotenv


class Alice:
    def __init__(self, lang):
        load_dotenv()
        city = os.getenv('city')
        key = os.getenv('api_key')
        self.weather = Weather_module(city, lang, key)
        self.voice = Voice(lang)
        self.processor = Phrase_analysis()
        self.chat = Chat_module()

    def run(self):
        while True:
            phrase = self.voice.listen()
            action, application = self.processor.analyse(phrase)
            print(action, application)
            if action is None and application is None:
                print("Couldn't understand")
            else:
                response = self.processor.get_response(action, application)
                print(f'Alice: {response}')
                self.voice.say(response)

            if action == 'start':
                self.action_start(application)
            elif action == 'get':
                self.action_get(application)
            elif action == 'quit':
                self.action_quit(application)
            elif action is None and (application != 'greeting' or application != 'farewell'):
                print('Unrecognized')

    def action_start(self, application):
        if application == 'cleaning':
            print('Not yet implemented')

        elif application == 'chat':
            phrase = self.voice.listen()
            if 'yes' in phrase:
                self.voice.say('Then we can start')
                while True:
                    phrase = self.voice.listen()
                    print(f'User: {phrase}')
                    action, application = self.processor.analyse(phrase)
                    print(action, application)
                    if action == 'quit' and application == 'chat':
                        response = self.processor.get_response(action, application)
                        print(f'Alice: {response}')
                        self.voice.say(response)
                        break
                    response = self.chat.get_response(phrase)
                    print(f'Alice: {response}')
                    self.voice.say(response)

    def action_get(self, application):
        if application == 'weather':
            response = self.weather.get_weather()
            self.voice.say(response)

    def action_quit(self, application):
        if application == 'cleaning':
            print('not yet implemented')
