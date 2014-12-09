import sys
from chatbot_helper import *

test = '''
I don't wanna "grow up"-- I'm a Toys 'R' us "kid". Don't you wanna lemme do the thing??
I have-to go (to) (the mall) [to] [eat a pancake] for {dinner} with the {emperor of Australia}!?
We're gonna "party all night" long like Jack&Janet and Nick & James. I've got $33.17 and
~everyone~ wants^2 `know where' and *what* that #green <thing> is. Samurai-Jack ate- only -three -
pancakes ''for'' his --lunch with-- Tiffany -- at the dog - park... 33% of the time, at least32
'''

def tokenize_test(string):
    print "started with string:", string
    tokens = tokenize(string)
    print "tokenized into", tokens
    output = process_response(tokens)
    print "resulting string:", output
    
if __name__ == '__main__':
#    tokenize_test('hi?!')
    tokenize_test(sys.argv[1])