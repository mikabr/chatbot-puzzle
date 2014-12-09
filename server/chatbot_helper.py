# -*- coding: utf-8 -*-
import string
from nltk.tokenize import RegexpTokenizer

remove_punct = {'[', ']', '{', '}', '⟨', '⟩', '<', '>', '~', '"', '`', '“', '”'}
space_before_punct = {'&', '#', '$', '-', '--'}
#contractions = {'t', 'll', 've', 'd', 'm', 's', 're', 'all', 'clock'}

def remove_punctuation(tokens):
    for i in xrange(len(tokens)):
        word = tokens[i]
        if word and word[0] == "'":
            word = word[1:]
        if word and word[-1] == "'":
            word = word[:-1]
        open = word.count('(')
        close = word.count(')')
        if open != close:
            word = word.replace('(', '')
            word = word.replace(')', '')
        tokens[i] = word
    return filter(lambda word: word != '', [filter(lambda char: char not in remove_punct, word) for word in tokens])

# given a list of words, sanitizes it to return something sentence-like
def process_response(response):

    # remove undesirable punctuation
    response = remove_punctuation(response)

    # remove any leading punctuation
    if response:
        first = 0
        for i in range(len(response)):
            if any([c not in string.punctuation for c in response[i]]):
                first = i
                break
        response = response[first:]

    # capitalize the first letter of the first word
    if response:
        response[0] = response[0].capitalize()

    output = response[0]
    # put the words into a string, inserting spaces where they should be
    for word in response[1:]:
        punct = word[0] in string.punctuation
        space = word[0] in space_before_punct
#        space = word[0] in space_before and filter(lambda c: c not in string.punctuation, word[1:]) not in contractions
        if not punct or space:
#        if not quote and (punct or (word[0] in space_before
#                                                                      and filter(lambda c: c not in string.punctuation, word[1:]) not in contractions)):
            output += ' '
        output += word

    return output

def tokenize(string):
    titles = 'Mr\.|Ms\.|Mrs\.|Dr\.'
    numbers = '\$[\d\.,]+|[\d,]+|[\d\.,]+\%|Fig\. [\d\.]+|'
    tk = RegexpTokenizer(titles + numbers + "[\w]+'[\w]+|'|\w+-\w+|--|-|\w+\(\S+\)|\(|\)|\w+|\S+")
    return tk.tokenize(string)
