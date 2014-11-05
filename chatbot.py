import random
import string
import re
import os
import nltk
from nltk.corpus import gutenberg


class ChatBot:

    def __init__(self, characters, corpora, models, ngram, estimator):
        self.characters = characters
        self.corpora = corpora
        self.estimator = estimator
        self.models = models
        self.n = ngram
#        self.models = {character: nltk.NgramModel(ngram, corp, estimator=self.estimator)
#                       for character, corp in self.corpora.iteritems()}

    @staticmethod
    def join_punctuation(seq, characters='.,;?!'):
        characters = set(characters)
        seq = iter(seq)
        current = next(seq)

        for nxt in seq:
            if nxt in characters:
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
        response = self.process_response(response, len(initial_words))
        if len(response) < 3:
            response = self.generate_response(character, seed)
        return response
#        num_words = random.choice(self.word_range)
#        initial_words = seed.split()
#        response = self.models[character].generate(num_words, context=initial_words)[len(initial_words):]
#        return ' '.join(response)

    @staticmethod
    def process_response(response, start):
        response = [word for word in response[start:]
                    if word not in {'(', ')', '[', ']', '{', '}', '\"', '`', '<', '>', '~'}]
        if response:
            if response[0] in string.punctuation:
                response = response[1:]
            response[0] = response[0].capitalize()
        response = ' '.join(response)
        return re.sub(r' (?=\W)', '', response)

    def score_character(self, character, inp):
        model = self.models[character]
        words = inp.split()
        if len(words) < self.n:
            for i in range(self.n - len(words)):
                model = model._backoff
        return model.entropy(inp.split())

    def classify_input(self, inp):
        scores = {character: self.score_character(character, inp) for character in self.characters}
        print scores
        best = min(scores, key=lambda c: scores[c])
        return best

    def pick_responder(self, input_character):
        return self.characters[(self.characters.index(input_character) + 1) % len(self.characters)]

    def run(self):
        print 'Talk with your new friends. Quit with Q or q.'
        while True:
            inp = raw_input('\n> ')
            if inp.lower() == 'q':
                break
            input_character = self.classify_input(inp)
            responder = self.pick_responder(input_character)
            print responder
            response = self.generate_response(responder, inp)
            print response


#corp = 'shakespeare-macbeth.txt'
#ChatBot.generate_respose(corp, "hello there")

test_chars = ['Austen', 'Carroll']
test_corpora = {'Austen': gutenberg.words('austen-emma.txt'),
                'Carroll': gutenberg.words('carroll-alice.txt')}

if __name__ == "__main__":

    chars = ['Nash', 'Orwell', 'Nixon', 'Aguilera']
    char_corps = {}
    for char in chars:
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
    bot = ChatBot(chars, char_corps, models, ngram=3, estimator=est)
    bot.run()

    #charsA = ['Nash', 'Orwell', 'Nixon', 'Aguilera', 'Rand', 'Yankovic']
    #chatbotA = ChatBot(charsA)
    #chatbotA.run()

    #charsB = ['Grande', 'Asimov', 'Marx', 'Einstein']
    #chatbotB = ChatBot(charsB)
