import sys
from chatbot_helper import *

def tokenize_test(string):
    print "started with string:", string
    tokens = tokenize(string)
    print "tokenized into", tokens
    output = process_response(tokens)
    print "resulting string:", output
    
if __name__ == '__main__':
    tokenize_test(sys.argv[1])