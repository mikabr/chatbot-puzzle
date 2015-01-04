import random
from chatbot import *

def simulate(bot, num_trials):

    correct = []
    response = "The quick brown fox jumps over the lazy dog."
    responder = random.choice(bot.characters)

#    print 'responder', responder
    for n in xrange(num_trials):

        tokens = tokenize(response)
        words = filter(lambda word: all([char not in string.punctuation.replace('-', '') for char in word]), tokens)
        response = bot.generate_response(responder, words)
#        print 'response', response

        classified_character = None
        if len(tokens) >= 8:
            classified_character = bot.classify_input(tokens)
#        print 'classified_character', classified_character

        correct.append(classified_character == responder)

        if classified_character:
            responder = bot.pick_responder(classified_character)
#        print 'responder', responder

    return correct

def simulate_char(bot, char, num_trials):

    correct = []
    response = "The quick brown fox jumps over the lazy dog."
#    responder = random.choice(bot.characters)

#    print 'responder', responder
    for n in xrange(num_trials):

        tokens = tokenize(response)
        words = filter(lambda word: all([char not in string.punctuation.replace('-', '') for char in word]), tokens)
        response = bot.generate_response(char, words)
#        print 'response', response

#        classified_character = None
#        if len(tokens) >= 8:
        classified_character = bot.classify_input(tokens)
#        print 'classified_character', classified_character

        correct.append(classified_character == char)

#        if classified_character:
#            responder = bot.pick_responder(classified_character)
#        print 'responder', responder

    return correct

#chars = ['Shakespeare', 'Nash', 'Asimov', 'Marx', 'Rand', 'Grande']
chars = ['Einstein', 'Nixon', 'Cyrus', 'Yankovic']
bot = initialize_bot(chars, None)
for char in chars:
    correct = simulate_char(bot, char, 100)
    print char, float(sum(correct)) / len(correct)