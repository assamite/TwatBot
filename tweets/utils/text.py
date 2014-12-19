'''
.. py:module:: text_utils
    :platform: Unix
    
Utility functions for working with texts.
'''
from collections import Counter
from textblob import TextBlob
from pattern.en import parse
from nltk.corpus import stopwords

def prettify(words):
    '''Prettify given iterable that represents words, part of words and
    other characters in the text::

    :param words: Sentence's words and other characters
    :type words: iterable
    :returns: str or unicode -- prettified text as one string
    '''
    #TODO: Kinda hackish code, which could be modified to use regex at some point.
    pretty_sentence = ""
    last_word = ""
    enc_hyphen = False
    
    for w in words:
        if w in ["``", "\""]:
            pretty_sentence += " \""
        elif w == "''":
            pretty_sentence += "\""
        elif w in [',', '!', '?', '.', '%', '\"', "n't", "'re", "'s", ";", ":", ")", "]", "}", "'m", "'ll", "'s", "'d", "\n"]:
            pretty_sentence += w
        elif w in ['\'']: 
            if enc_hyphen:
                pretty_sentence += w
                enc_hyphen = False    
        elif last_word in ["``", "(", "[", "{", "\""]:
            pretty_sentence += w    
        else:
            pretty_sentence += " " + w
        if w.startswith("'") and w not in ["'m", "'d", "'re", "'s", "'ll"]: 
            enc_hyphen = True
        last_word = w
    
    pretty_sentence = pretty_sentence.strip()
    return pretty_sentence[0].upper() + pretty_sentence[1:]


def same_words(sentence1, sentence2):
    '''Amount of same words in sentences. 
    
    Some stop words are excluded from the count.
    '''
    stops = {'a', 'an', 'the', 'of', 'in'}
    A = set(TextBlob(sentence1.lower()).words) - stops
    B = set(TextBlob(sentence2.lower()).words) - stops
    return len(A & B)
    

def sentiment(text):
    '''Text's sentiment analysis.
    
    Calculates the mean sentiment of the sentences in the text. Sentiment is 
    returned as a (subjectivity, polarity)-tuple of floats, where subjectivity
    is in [0, 1] and polarity in [-1, 1].
    
    :param text: Text to analyze.
    :type text: str or unicode
    :returns: tuple -- (subjectivity, polarity) 
    '''
    sent = [0.0, 0.0]
    blob = TextBlob(text)  
    for s in blob.sentences:
        sent[0] += s.sentiment.subjectivity
        sent[1] += s.sentiment.polarity
     
    sent[0] /= len(blob.sentences)  
    sent[1] /= len(blob.sentences) 
    return tuple(sent)


def bag_of_words(text, counts = False):
    '''Extract bag-of-words from given text.
    
    Typical English stopwords are excluded from the bag-of-words.
    
    :param text: Text to extract bag-of-words
    :returns: list -- words, if counts is True then word, count pairs in descending count order
    '''
    sentences = parse(text.lower(), lemmata = True, tags = False, chunks = False).split()
    words = reduce(lambda x,y: x + y, sentences, [])
    words = reduce(lambda x,y: x + [y[0]], filter(lambda x: len(x[0]) > 2, words), [])
    ctr = Counter(words)
    sw = set(stopwords.words('english'))
    for c in ctr.keys():
        if c in sw:
            del ctr[c]
    
    if counts:
        ret = sorted(ctr.items(), key = lambda x: x[1], reverse = True)
    else:
        ret = ctr.keys()
    return ret


def bow(text, counts = False):
    '''Shorthand for :py:func:`bag_of_words`.
    '''
    return bag_of_words(text, counts)


def get_NNPs(text, counts = False):
    '''Extract proper nouns from text.
    
    :param text: Text to parse
    :type text: str
    :param counts: Return counts for each extracted NNP
    :type counts: bool
    :returns: list -- List containing either only the extracted NNP's or (NNP, count) -pairs sorted by count.
    '''
    parsed_text = parse(text).split()
    nnps = [] 
    for sent in parsed_text:
        for word in sent:
            if word[1].startswith('NNP'):
                nnps.append(word[0])
                
    ctr = Counter(nnps)
    if counts:
        ctri = ctr.items()
        ctri = sorted(ctri, key = lambda x: x[1], reverse = True)
    else:
        ctri = ctr.keys()
    return ctri
    
    