import json
import string
import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout


class Language_processing:
    def __init__(self):
        with open('processing/nlp_data.json', 'r') as key:
            self.data = json.loads(key.read())

        nltk.download('omw-1.4')
        nltk.download("punkt")
        nltk.download("wordnet")

        self.lemmatizer = WordNetLemmatizer()

        self.words = []
        self.classes = []
        self.doc_X = []
        self.doc_y = []

        for intent in self.data["intents"]:
            for pattern in intent["patterns"]:
                tokens = nltk.word_tokenize(pattern)
                self.words.extend(tokens)
                self.doc_X.append(pattern)
                self.doc_y.append(intent["tag"])

            if intent["tag"] not in self.classes:
                self.classes.append(intent["tag"])

        new_word = []
        for word in self.words:
            if word not in string.punctuation:
                new_word.append(self.lemmatizer.lemmatize(word.lower()))
        self.words = new_word

        self.words = sorted(set(self.words))
        self.classes = sorted(set(self.classes))
        self.training = []
        self.out_empty = [0] * len(self.classes)
        self.train_X = []
        self.train_Y = []
        self.model = None

    def create_dataset(self):
        for idx, doc in enumerate(self.doc_X):
            bow = []
            text = self.lemmatizer.lemmatize(doc.lower())
            for word in self.words:
                bow.append(1) if word in text else bow.append(0)

            output_row = list(self.out_empty)
            output_row[self.classes.index(self.doc_y[idx])] = 1

            self.training.append([bow, output_row])

        random.shuffle(self.training)
        self.training = np.array(self.training, dtype=object)

        self.train_X = np.array(list(self.training[:, 0]))
        self.train_Y = np.array(list(self.training[:, 1]))

    def build_and_train_model(self):
        input_shape = (len(self.train_X[0]),)
        output_shape = len(self.train_Y[0])

        model = Sequential()
        model.add(Dense(128, input_shape=input_shape, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.3))
        model.add(Dense(output_shape, activation="softmax"))
        adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
        model.compile(loss='categorical_crossentropy',
                      optimizer=adam,
                      metrics=["accuracy"])
        print(model.summary())
        hist = model.fit(x=self.train_X, y=self.train_Y, epochs=200, verbose=1)
        model.save('ai_storage/alice_v1.h5', hist)
        model.save_weights('ai_storage/weights/alice_weights_v1')

    def load_model(self):
        self.model = tf.keras.models.load_model('ai_storage/alice_v1.h5')
        self.model.load_weights('ai_storage/weights/alice_weights_v1')

    def clean_phrase(self, phrase):
        words_in_phrase = nltk.word_tokenize(phrase)
        words_in_phrase = [self.lemmatizer.lemmatize(word) for word in words_in_phrase]
        return words_in_phrase

    def bag_of_words(self, phrase):
        tokens = self.clean_phrase(phrase)
        bow = [0] * len(self.words)
        for w in tokens:
            for idx, word in enumerate(self.words):
                if word == w:
                    bow[idx] = 1
        return np.array(bow)

    def pred_class(self, text):
        if text == '__Error__':
            return ['__Error__']
        bow = self.bag_of_words(text)
        result = self.model.predict(np.array([bow]))[0]
        thresh = 0.2
        y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

        y_pred.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in y_pred:
            return_list.append(self.classes[r[0]])
        return return_list

    def get_response(self, intents_list):
        result = ''
        tag = intents_list[0]
        list_of_intents = self.data["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                break

        if result == '' or intents_list == ['__Error__']:
            result = "error"
        return result


