import warnings
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random
from keras.models import load_model


class Language_processing:
    def __init__(self):
        warnings.filterwarnings("ignore")

        self.lemmatizer = WordNetLemmatizer()

        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_words = ['?', '!']
        data_file = open("nlp_data.json").read()
        self.intents = json.loads(data_file)

        nltk.download('punkt')
        nltk.download('wordnet')

        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                self.documents.append((w, intent['tag']))

                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [self.lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

        print(len(self.documents), "documents")
        print(len(self.classes), "classes", self.classes)
        print(len(self.words), "unique lemmatized words", self.words)

        pickle.dump(self.words, open('words.pkl', 'wb'))
        pickle.dump(self.classes, open('classes.pkl', 'wb'))
