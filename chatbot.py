import random
import string
import re
import os
import nltk
from nltk.corpus import gutenberg


class ChatBot:

    def __init__(self, characters, models, ngram):
        self.characters = characters
        self.models = models
        self.n = ngram

    @staticmethod
    def join_punctuation(seq, punct='.,;?!'):
        charpunctacters = set(punct)
        seq = iter(seq)
        current = next(seq)

        for nxt in seq:
            if nxt in punct:
                current += nxt
            else:
                yield current
                current = nxt

    def generate_response(self, character, seed):
        model = self.models[character]
        initial_words = seed.split()
        response = seed.split()
        while response and not response[-1][-1] in {'.', '!', '?', '?!'}:
            word = model._generate_one(response)
            response.append(word)
        print response
        response = self.process_response(response[len(initial_words):])
        print response
        if len(response) < 3:
            response = model.generate_response
        return response

    # given a list of words, sanitizes it to return something sentence-like
    @staticmethod
    def process_response(response):

        # removes potentially unmatched punctuation
        response = [word for word in response if word not in {'(', ')', '[', ']', '{', '}', '\"', '`', '<', '>', '~'}]

        if response:

            # removes any leading punctuation
            if response[0] in string.punctuation:
                response = response[1:]

            # capitalizes the first letter of the first word
            response[0] = response[0].capitalize()

        # puts the words into a string, with spaces between words but not before punctuation
        response = ' '.join(response)
        response = re.sub(r' (?=\W)', '', response)
        return response

    # given a character and an input string, scores how similar the string is to that character's corpus
    # return cross-entropy between character's corpus and input string
    def score_character(self, character, inp):
        model = self.models[character]
        if len(words) < self.n:
            for i in range(self.n - len(words)):
                model = model._backoff
        return model.entropy(nltk.word_tokenize(inp))

    # given an input string, scores it's similarity to each character and selects min scoring character
    def classify_input(self, inp):
        scores = {character: self.score_character(character, inp) for character in self.characters}
        print scores
        best = min(scores, key=lambda c: scores[c])
        return best

    # given a character, returns the next character in the characters list (wrapping last to first)
    def pick_responder(self, input_character):
        return self.characters[(self.characters.index(input_character) + 1) % len(self.characters)]

    # runs chatbot input/response interface
    def run(self):

        print 'Talk with your new friends. Quit with Q or q.'

        while True:

            # get input from user
            inp = raw_input('\n> ')
            if inp.lower() == 'q':
                break

            # classify input as character it's most similar to
            input_character = self.classify_input(inp)

            # deterministically pick character to respond as
            responder = self.pick_responder(input_character)
            print responder

            # generate response from selected character, seeded with user's input
            response = self.generate_response(responder, inp)
            print response

def initialize_bot(characters):

    char_corps = {}
    for char in characters:
        assert(char in os.listdir('TrainingSets/'))
        print 'loading', char
        corpus = []
        for datafile in os.listdir('TrainingSets/' + char):
            data = open('TrainingSets/' + char + '/' + datafile, 'r').read()
            data = nltk.word_tokenize(data)
            corpus += data
        char_corps[char] = corpus
    est = lambda fdist, bins: nltk.probability.LidstoneProbDist(fdist, 0.2)
    models = {character: nltk.NgramModel(3, corp, estimator=est)
              for character, corp in char_corps.iteritems()}
    bot = ChatBot(chararacters, models, ngram=3)
    return bot


if __name__ == "__main__":
    chars = ['Nash', 'Orwell', 'Nixon', 'Aguilera']
    bot = initialize_bot(chars)
    bot.run()
