import json
import random


class Phrase_analysis:
    def __init__(self):
        with open('voice/actions.json', 'r') as key:
            self.actions = json.loads(key.read())
        with open('voice/applications.json', 'r') as key:
            self.applications = json.loads(key.read())
        with open('voice/responses.json', 'r') as key:
            self.requests = json.loads(key.read())

    def analyse(self, phrase):
        output_action = None
        output_application = None
        for action in self.actions["actions"]:
            for pattern in action["patterns"]:
                if pattern in phrase:
                    output_action = action["tag"]

        for application in self.applications["applications"]:
            for pattern in application["patterns"]:
                if pattern in phrase:
                    output_application = application["tag"]

        return output_action, output_application

    def get_response(self, action, application):
        if action is None:
            action = ''
        if application is None:
            application = ''
        tag = action + ' ' + application
        for request in self.requests["requests"]:
            if tag == request["tag"]:
                response = random.choice(request["response"])

                return response
