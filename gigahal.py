# Depends on pymarkovchain, itertools, os, re, glob

from pymarkovchain import MarkovChain
from itertools import tee, izip
import os
import re
import math
from glob import glob

DEBUG=False

class Character:
    def __init__(self,name,directory,dbpath,reloaddb=False,debug=False):
        self.name = name
        self.partner = None
        self.directory = directory
        self.dbpath = dbpath
        self.reloaddb = reloaddb
        self.debug = debug
        self.db = self.getMarkovChainGenerator()

    def getMarkovChainGenerator(self):
        db = MarkovChain(self.dbpath)
        if self.reloaddb or not os.path.exists(self.dbpath):
            files = glob(os.path.join(self.directory,'*.txt'))
            text = []
            for path in files:
                with open(path,"rb") as f:
                    text.append(f.read())

#            alltext = re.sub(r'\n+',' ','\n'.join(text),flags=re.MULTILINE)
            alltext = '\n'.join(text)
            if self.debug:
                print alltext
            if self.debug:
                print files
            db.generateDatabase(alltext.lower(),'[\:.!?\n,;-]+')
            db.dumpdb()
        return db
    
    def getScore(self,string,debug=False):
        score = 0
        string = string.lower().split() + ['']

        if len(string) == 0:
            return 0

        if debug:
            print self.name,':'
        for word, word2 in pairwise(string):
            word_score = 0
            if self.db.db.has_key(word):
                prob = self.db.db[word]
                if prob.has_key(word2):
                    word_score = prob[word2]#*math.sqrt(len(prob))
            else:
                if self.debug:
                    print 'Word not found in chain : ',word
                word_score = -0.5
            if debug:
                print '\t',word,' : ',word_score
            score += word_score
        
        return score/len(string)


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def test(db):
    test_string0 = "I came in like a wrecking ball"
    test_string1 = "How called you the man"
    test_string2 = "You are a fishmonger"

    score0 = getScore(db,test_string0,debug=DEBUG)
    score1 = getScore(db,test_string1,debug=DEBUG)
    score2 = getScore(db,test_string2,debug=DEBUG)
    
    print test_string0," : ",score0
    print test_string1," : ",score1
    print test_string2," : ",score2

def identify_player(string,dblist):
    return max(dblist,key=lambda x: x.getScore(string))
    
shakespeare = Character("Shakespeare","./TrainingSets/Shakespeare","./shakespeareDB",reloaddb=True)
cyrus = Character("Cyrus","./TrainingSets/Cyrus","./cyrusDB",reloaddb=True)
shakespeare.partner = cyrus
cyrus.partner = shakespeare

character_list = [shakespeare,cyrus]

def main():
    print 'Talk with your new friends. Quit with Q or q.'
    while(True):
        inp = raw_input('\n> ')
        if inp.lower() == 'q':
            break
        responder = identify_player(inp.lower(),character_list).partner
        response = responder.db.generateStringWithSeed(inp)
        response = response[len(inp)+1:]
        # Make sure the response is at least 8 words long
        counter = 0
        while len(response.split(' ')) < 8:
            new_response_part = ''
            if response == '' or response == ' ':
                response = responder.db.generateStringWithSeed(inp)
            if len(response.split(' ')) == 1:
                new_response_part += responder.db.generateStringWithSeed(response)
                if len(new_response_part.split(' ')) > 0:
                    new_response_part = new_response_part[len(response)+1:]
            else:
                old_response_end = ' '.join(response.split(' ')[-2:])
                new_response_part += responder.db.generateStringWithSeed(old_response_end)
                if len(new_response_part.split(' ')) > 0:
                    new_response_part = new_response_part[len(old_response_end)+1:]
#            print '\t',new_response_part

            if not new_response_part in response:
#                print new_response_part, ' ', response
                response += ' '
                response += new_response_part

            #For some reason it seems like this occasionally gets stuck unable to find the next thing to say. If that's the case, just choose a random response
            if counter > 100:
                response = responder.db.generateString()
                
            counter += 1

#        print responder.name," : ",response
        print response

if __name__ == '__main__':
    main()
#identify_player("I came in like a wrecking ball",character_list)
#identify_player("How called you the man",character_list)
#identify_player("You are a fishmonger",character_list)
