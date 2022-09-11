from voice.voice import Voice
from voice.chat_module import Chat_module
from processing.weather import Weather_module
from processing.phrase_analysis import Phrase_analysis
from cleaning.clean import Cleaning
from dotenv import load_dotenv
from logger import LoggingHandler
import os


class Alice(LoggingHandler):
    def __init__(self, lang):
        super().__init__()
        self.log.info(f'Launching Alice')
        load_dotenv()
        self.log.info(f'Loaded environment')
        city = os.getenv('city')
        key_weather = os.getenv('weather_key')
        key_ifttt = os.getenv('ifttt_key')
        start_clean_name = os.getenv('alice_start_cleaning')
        stop_clean_name = os.getenv('alice_stop_cleaning')
        self.log.info(f'Loaded api keys')
        self.weather = Weather_module(city, lang, key_weather)
        self.log.info(f'Weather module connected')
        self.cleaning = Cleaning(key_ifttt, start_clean_name, stop_clean_name)
        self.log.info(f'Cleaning module connected')
        self.voice = Voice(lang)
        self.log.info(f'Voice module connected')
        self.processor = Phrase_analysis()
        self.log.info(f'Processing module connected')
        self.chat = Chat_module()
        self.log.info(f'Chat module connected')
        self.log.info(f'Alice setup complete')

    def run(self):
        while True:
            phrase = self.voice.listen()
            action, application = self.processor.analyse(phrase)

            if action == 'start':
                self.action_start(application)
            elif action == 'get':
                self.action_get(application)
            elif action == 'quit':
                self.action_quit(application)
            elif action is None and (application != 'greeting' and
                                     application != 'farewell' and
                                     application != 'introduction'):
                print('Unrecognized')
                self.log.warning(f'Unrecognized')

            if action is None and (application == 'greeting' or
                                   application == 'farewell' or
                                   application == 'introduction'):
                response = self.processor.get_response('', application)
                self.voice.say(response)

    def action_start(self, application):
        if application == 'cleaning':
            self.log.info(f'Starting cleaning')
            response = self.processor.get_response('start', application)
            self.voice.say(response)
            self.cleaning.start_cleaning()

        elif application == 'chat':
            response = self.processor.get_response('start', application)
            self.voice.say(response)
            phrase = self.voice.listen()
            if 'yes' in phrase:
                self.log.info(f'Started chatting mode')
                self.voice.say('Then we can start')
                while True:
                    phrase = self.voice.listen()
                    action, application = self.processor.analyse(phrase)
                    if action == 'quit' and application == 'chat':
                        self.log.info(f'Exiting chat mode')
                        response = self.processor.get_response(action, application)
                        self.voice.say(response)
                        break
                    response = self.chat.get_response(phrase)
                    self.voice.say(response)

    def action_get(self, application):
        if application == 'weather':
            self.log.info(f'Obtaining weather')
            response = self.processor.get_response('get', application)
            self.voice.say(response)
            response = self.weather.get_weather()
            self.voice.say(response)

    def action_quit(self, application):
        if application == 'cleaning':
            self.log.info(f'Stopping cleaning')
            response = self.processor.get_response('quit', application)
            self.voice.say(response)
            self.cleaning.stop_cleaning()
