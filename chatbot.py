import random
import string
import re
import os
import nltk
from nltk.probability import *
from ngram import NgramModel
#from kneserney import KneserNeyProbDist


class ChatBot:

    def __init__(self, characters, models, ngram, debug=False):
        self.characters = characters
        self.models = models
        self.n = ngram
        self.debug = debug

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
        response = self.process_response(response[len(initial_words):])
#        if len(response) < 3:
#            response = self.generate_response(character, seed)
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
    def score_character(self, character, words):
        model = self.models[character]
        if len(words) < self.n:
            for i in range(self.n - len(words)):
                model = model._backoff
        return model.entropy(words)

    # given an input string, scores it's similarity to each character and selects min scoring character
    def classify_input(self, inp):
        words = nltk.word_tokenize(inp)
        scores = {character: self.score_character(character, words) for character in self.characters}
        scores = {character: score for character, score in scores.iteritems() if score}
        if self.debug:
            print scores
        if scores:
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
            if self.debug:
                print input_character
                
            if input_character:

                # deterministically pick character to respond as
                responder = self.pick_responder(input_character)
    
                # generate response from selected character, seeded with user's input
                response = self.generate_response(responder, inp)
                print response
                
            else:

                print "That's not very interesting..."

def load_corpora(characters):

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
    return char_corps
#    return models


if __name__ == "__main__":
    n = 3
    chars = ['Nash', 'Orwell', 'Nixon', 'Aguilera', 'Rand', 'Yankovic']
#    chars = ['Grande', 'Asimov', 'Marx', 'Einstein']
    char_corps = load_corpora(chars)
    est = lambda fdist, bins: MLEProbDist(fdist)
#    est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
#    est = lambda fdist, bins: WittenBellProbDist(fdist)
#    est = lambda fdist, bins: KneserNeyProbDist(fdist)
    models = {character: NgramModel(n, corp, estimator=est)
              for character, corp in char_corps.iteritems()}
    bot = ChatBot(chars, models, ngram=n, debug=False)
    bot.run()
