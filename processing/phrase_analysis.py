import json
import random
from logger import LoggingHandler


class Phrase_analysis(LoggingHandler):
    def __init__(self):
        super().__init__()
        with open('voice/actions.json', 'r') as key:
            self.log.info(f'Loading {key}')
            self.actions = json.loads(key.read())
        with open('voice/applications.json', 'r') as key:
            self.log.info(f'Loading {key}')
            self.applications = json.loads(key.read())
        with open('voice/responses.json', 'r') as key:
            self.log.info(f'Loading {key}')
            self.requests = json.loads(key.read())

    def analyse(self, phrase):
        self.log.info(f'Got input: {phrase}')
        output_action = None
        output_application = None
        for action in self.actions["actions"]:
            for pattern in action["patterns"]:
                if pattern in phrase:
                    output_action = action["tag"]
                    self.log.info(f'Action found: {output_action}')

        for application in self.applications["applications"]:
            for pattern in application["patterns"]:
                if pattern in phrase:
                    output_application = application["tag"]
                    self.log.info(f'Application found: {output_application}')

        self.log.info(f'Outputting: action {output_action}, application: {output_application}')
        return output_action, output_application

    def get_response(self, action, application):
        self.log.info(f'Getting response with action {action}, application {application}')
        if action is None:
            action = ''
        if application is None:
            application = ''
        tag = action + ' ' + application
        self.log.info(f'Tag generated: {tag}')
        for request in self.requests["requests"]:
            if tag == request["tag"]:
                response = random.choice(request["response"])
                self.log.info(f'Chosen response: {response}')

                return response
