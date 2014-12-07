# -*- coding: utf-8 -*-
import string
from nltk.tokenize import RegexpTokenizer

remove_punct = {'(', ')', '[', ']', '{', '}', '⟨', '⟩', '<', '>', '~', '"', '`', '–', '“', '”'}
space_before = {'&', '#', '$', "'", "’"}
contractions = {'t', 'll', 've', 'd', 'm', 's', 're', 'all', 'clock'}

def remove_punctuation(string):
    return filter(lambda word: word != '', [filter(lambda char: char not in remove_punct, word) for word in string])

# given a list of words, sanitizes it to return something sentence-like
def process_response(response):

    # remove undesirable punctuation
    response = remove_punctuation(response)

    # remove any leading punctuation
    if response:
        first = 0
        for i in range(len(response)):
            if all([c not in string.punctuation for c in response[i]]):
                first = i
                break
        response = response[first:]

    # capitalize the first letter of the first word
    if response:
        response[0] = response[0].capitalize()

    output = response[0]
    # put the words into a string, inserting spaces where they should be
    for word in response[1:]:
        if (word[0] not in string.punctuation) or (word[0] in space_before
                                                   and filter(lambda c: c not in string.punctuation, word[1:]) not in contractions):
            output += ' '
        output += word

    return output

def tokenize(string):
    tk = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    return tk.tokenize(string)
