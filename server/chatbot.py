import os
import subprocess
from nltk.probability import *
from ngram import NgramModel
from chatbot_helper import *


class ChatBot:

    def __init__(self, characters, nicknames, models, ngram, debug=False):
        self.characters = characters
        self.nicknames = nicknames
        self.models = models
        self.n = ngram
        self.debug = debug

    def generate_response(self, character, seed):
        model = self.models[character]
        response = seed[:]
        end = {'.', '!', '?', '?!'}
        while len(response) < (8 + len(seed)):
            word = model._generate_one(response)
            response.append(word)
        while response[-1] not in end and len(response) < 25:
            word = model._generate_one(response)
            response.append(word)
        if response[-1] not in end:
            response.append('.')
        response = response[len(seed):]
        response = process_response(response)
#        if len(tokenize(response)) < 3 or all([char in string.punctuation for char in response]):
#            response = self.generate_response(character, seed)
        return response

    # given a character and an input string, scores how similar the string is to that character's corpus
    # return cross-entropy between character's corpus and input string
    def score_character(self, character, words):
        model = self.models[character]
        if len(words) < self.n:
            for i in range(self.n - len(words)):
                model = model._backoff
        if self.debug:
            print model
        return model.entropy(words)

    # given an input string, scores it's similarity to each character and selects min scoring character
    def classify_input(self, words):
        # try:
        #     directory = os.path.join(os.path.dirname(__file__), 'TrainingSets/')
        #     search = subprocess.check_output(["grep", "-r", "-i", ' '.join(words), directory])
        #     results = [result.split(':')[0].split('/')[1] for result in search.split('\n') if ':' in result]
        #     if results and all([result == results[0] for result in results[1:]]) and results[0] in self.characters:
        #         return results[0]
        # except:
        #     pass
        scores = {}
        if words:
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

#    def response(self, inp, current):
#        current = current % len(self.characters)
    def response(self, inp):

        print inp
        tokens = tokenize(inp)
#        if len(tokens) < 5:
#            return "Can you say more?"

        input_character = self.classify_input(tokens)
        if not input_character:
            return "That doesn't sound like something any of us would say...", "Nobody"

        # deterministically pick character to respond as
#        responder = self.pick_responder(input_character)
        responder = input_character

        # generate response from selected character, seeded with user's input
        words = filter(lambda word: all([char not in string.punctuation.replace('-', '') for char in word]), tokens)
        response = self.generate_response(responder, words)
        nickname = self.nicknames[input_character]
#        intro = self.intros[self.current_intro]
#        self.current_intro = (self.current_intro + 1) % len(self.intros)
#        intro = "Hi"
#        message = "%s %s! %s" % (intro, nickname, response)

#        return message
        return response, nickname

    # runs chatbot input/response interface
    def run(self):

        print 'Talk with your new friends. Quit with Q or q.'

        while True:

            # get input from user
            inp = raw_input('\n> ')
            if inp.lower() == 'q':
                break

#            response = self.response(inp, character)
            response, responder = self.response(inp)
            print responder + ': ' + response

def load_corpora(characters):

    char_corps = {}
    for char in characters:
        directory = os.path.join(os.path.dirname(__file__), 'TrainingSets/')
        assert(char in os.listdir(directory))
        corpus = []
        for datafile in os.listdir(directory + char):
            data = open(directory + char + '/' + datafile, 'r').read()
            data = tokenize(data)
            corpus += data
        char_corps[char] = corpus
    return char_corps
#    return models

def initialize_bot(chars, nicks):
    n = 3
#    intros = ["So", "Hi", "In fact", "For what it's worth", "Think about it",
#              "Conversely", "On the other hand", "Debatably", "Especially", "Not to mention", "Although", "Moreover", "Equally",
#              "But", "Yes",
#              "See here", "Ultimately", "Rather", "Nevertheless", "As you said", "Mind you", "Even so"]
    char_corps = load_corpora(chars)
    est = lambda fdist, bins: MLEProbDist(fdist)
#    est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
#    est = lambda fdist, bins: WittenBellProbDist(fdist)
#    est = lambda fdist, bins: KneserNeyProbDist(fdist)
    models = {character: NgramModel(n, corp, estimator=est)
              for character, corp in char_corps.iteritems()}
#    return ChatBot(chars, nicks, intros, models, ngram=n, debug=False)
    return ChatBot(chars, nicks, models, ngram=n, debug=False)


class memorize(dict):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result

@memorize
def bot():
    print 'Initializing bot'
    chars = ['Whitman', 'Nixon', 'Rand', 'Nash', 'Aguilera', 'Shakespeare']
    nicks = {'Whitman': 'Wonderland', 'Nixon': 'Tulip', 'Rand': 'Threesome',
             'Nash': 'Wonton', 'Aguilera': 'Sick Soup', 'Shakespeare': 'Tentacle'}
    return initialize_bot(chars, nicks)

# @memorize
# def bot1():
#     print 'Initializing bot1'
#     chars = ['Nash', 'Nixon', 'Rand', 'Marx', 'Shakespeare', 'Cyrus']
#     nicks = {'Nash': 'Wonton', 'Nixon': 'Forehead', 'Rand': 'Threesome', 'Marx': 'Toothbrush',
#              'Shakespeare': 'Tentacle', 'Cyrus': 'Tupac'}
#     return initialize_bot(chars, nicks)
# #    print 'Initialized bot1'
#
# @memorize
# def bot2():
#     print 'Initializing bot2'
#     chars = ['Grande', 'Yankovic', 'Asimov', 'Einstein']
#     nicks = {'Grande': 'Wonder Woman', 'Yankovic': 'Tulip', 'Asimov': 'Foreigner', 'Einstein': 'Sick Soup'}
#     return initialize_bot(chars, nicks)
#    print 'Initialized bot2'

if __name__ == "__main__":
    print 'Please wait...'
    bot().run()
