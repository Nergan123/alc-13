import json


class Speech_processor:

    fields = [
        'kenobi',
        'greeting',
        'farewell'
    ]

    def __init__(self):
        with open('processing/keywords.json', 'r') as key:
            data = json.loads(key.read())
        for property_name in self.fields:
            self.__setattr__(property_name, data[property_name])

    def choose_action(self, phrase):
        for field in self.fields:
            current_field = self.__getattribute__(field)
            for keyword in current_field:
                if keyword in phrase:
                    return field

        return 'Unknown'

    @staticmethod
    def generate_response(field):
        if field == 'kenobi':
            return 'General Kenobi'
        elif field == 'greeting':
            return 'And good day to you, dear sir'
        elif field == 'farewell':
            return 'I hope to see you later'
        else:
            return "Sorry master, I didn't understand it"
