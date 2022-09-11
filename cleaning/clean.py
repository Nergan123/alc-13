import requests
from logger import LoggingHandler


class Cleaning(LoggingHandler):
    def __init__(self, api_key, start_clean_name, stop_clean_name):
        super().__init__()
        self.log.info(f'Setting up Cleaning module')
        self.key = api_key
        self.start_name = start_clean_name
        self.stop_name = stop_clean_name
        self.log.info(f'Cleaning module setup complete')

    def start_cleaning(self):
        self.log.info(f'Requesting cleaning')
        r = requests.post(f'https://maker.ifttt.com/trigger/{self.start_name}/with/key/{self.key}')
        self.log.info(f'Got response: {r.status_code}, {r.reason}')

    def stop_cleaning(self):
        self.log.info(f'Requesting cleaning stop')
        r = requests.post(f'https://maker.ifttt.com/trigger/{self.stop_name}/with/key/{self.key}')
        self.log.info(f'Got response: {r.status_code}, {r.reason}')
