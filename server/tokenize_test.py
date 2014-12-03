import sys
from chatbot import *
from nltk.tokenize import RegexpTokenizer

def tokenize_test(string):
    tk = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    output = ChatBot.process_response(tk.tokenize(string))
    print "started with string:", string
    print "resulting string:", output
    
if __name__ == '__main__':
    tokenize_test(sys.argv[1])