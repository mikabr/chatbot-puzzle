import string
from nltk.tokenize import regexp_tokenize

space_before_punct = {'&', '#', '$', '-', '--', '=', '+', '*'}
#contractions = {'t', 'll', 've', 'd', 'm', 's', 're', 'all', 'clock'}

def remove_punctuation(tokens):

    remove_punct = {'[', ']', '{', '}', '<', '>', '~', '"', '`'}
    allowed = string.letters + string.digits + string.punctuation
    for char in remove_punct:
        allowed = allowed.replace(char, '')

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

    return filter(lambda word: word != '', [filter(lambda char: char in allowed, word) for word in tokens])

# given a list of words, sanitizes it to return something sentence-like
def process_response(response):

    # remove any non-printable characters
    response = map(lambda w: filter(lambda c: c in string.printable, w), response)

    # remove undesirable punctuation
    response = remove_punctuation(response)

    # remove any leading punctuation
    if response:
        first = 0
        for i in range(len(response)):
            if any([c in string.letters for c in response[i]]):
                first = i
                break
        response = response[first:]

    # remove any trailing punctuation except for the sentence end mark
    if response:
        last = -1
        for i in reversed(range(len(response)-1)):
            if not all([char in string.punctuation for char in response[i]]):
                last = i+1
                break
        response = response[:last] + [response[-1]]

    # capitalize the first letter of the first word
    if response:
        response[0] = response[0].capitalize()

    output = response[0]
    # put the words into a string, inserting spaces where they should be
    for word in response[1:]:
        if word[0] not in string.punctuation or word[0] in space_before_punct or (word[0] == '.' and len(word) > 1):
            output += ' '
        output += word

    return output

def tokenize(string):
    titles = 'Mr\.|Ms\.|Mrs\.|Dr\.|'
    numbers = '\$[\d\.,]+|[\d,]+|[\d\.,]+\%|Fig\. [\d\.]+|#\d+|'
    pattern = titles + numbers + "[\w]+'[\w]+|'|\w+-\w+|--|-|\w+\(\S+\)|\(|\)|\.|\*|\+|\w+|\S+"
    return regexp_tokenize(string, pattern)
