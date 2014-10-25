'''
.. py:module:: text_utils
    :platform: Unix
    
Some utility functions for working with texts.
'''
from textblob import TextBlob

def prettify_sentence(words):
    """Prettify given iterable that represents words and part of words and
    other characters of the sentence. ie, there can be indeces with only
    "'ll" or "'" in them.
    
    Kinda hackish code, which could be looked into in some point of time.
    
    **Args:**
        | words (iterable): Iterable with sentence's words and other characters. This iterable is considered to be created by nltk >=2.04 part of speech tagging (and replacing some words in it).
        
    **Returns:**
        str or unicode, prettified sentence as one string.
    """
    pretty_sentence = ""
    last_word = ""
    enc_hyphen = False
    
    for w in words:
        if w in ["``", "\""]:
            pretty_sentence += " \""
        elif w == "''":
            pretty_sentence += "\""
        elif w in [',', '!', '?', '.', '%', '\"', "n't", "'re", "'s", ";", ":", ")", "]", "}", "'m", "'ll", "'s", "'d"]:
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
    """Amount of same words in sentences. 
    
    Some stop words are excluded from the count.
    """
    stops = {'a', 'an', 'the', 'of', 'in'}
    A = set(TextBlob(sentence1.lower()).words) - stops
    B = set(TextBlob(sentence2.lower()).words) - stops
    return len(A & B)
    

def sentiment(text):
    """Text's sentiment analysis.
    
    Calculates a sum of all the text's sentences sentiment.
    
    **Args:**
        | text (str or unicode): Text to analyse
        
    **Returns:**
        Tuple (subjectivity, polarity), where subjectivity is float in [0, 1]
        and polarity is float in [-1, 1]. 
    """
    sent = [0.0, 0.0]
    blob = TextBlob(text)  
    for s in blob.sentences:
        sent[0] += s.sentiment.subjectivity
        sent[1] += s.sentiment.polarity
     
    sent[0] /= len(blob.sentences)   
    return tuple(sent)
