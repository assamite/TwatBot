'''
.. py:module:: sentence
    :platform: Unix
    
Text generation for new age context.
'''
import random
import re
from vocab import *


def _random_word(pos):
    r = random.randint(0, len(vocabs[pos]) - 1)
    return vocabs[pos][r]


def _fix_format(sentence):
    sentence = sentence.strip()
    # Capitalize
    sentence = sentence[0].upper() + sentence[1:]
    # Add last punctuation if missing.
    if sentence[-1] not in '.!?':
        sentence += '.';
    
    # Strip possible spaces before punctuation
    result = re.sub('( [,.;\?!])', lambda x: x.group(0)[-1], sentence);
    # Try to fix 'a epic' to 'an epic'. Not fool proof as naively only considers
    # if the next word starts with a vowel or not.
    result = re.sub('(^|\W)([Aa]) ([aeiou])', lambda x: x.group(1)+x.group(2)+"n "+x.group(3), result)
    # take care of prefixes (delete the space after the hyphen)
    result = re.sub('([^- ])- ', lambda x: x.group(1)+'-', result);
    return result


def generate_sentence():
    template = random.choice(templates)
    template = re.sub('[.,;?!]', lambda x: " "+x.group(0), template)
    template = template.split(" ")
    result = ""
    
    for s in template:
        if s in vocabs:
            result += _random_word(s)
        else:
            result += s;
        result += ' ';
    
    return _fix_format(result)


def generate_text(ns):
    text = reduce(lambda x,y: " ".join([x, generate_sentence()]), xrange(ns), "")
    return text.strip()


if __name__ == '__main__':
    print generate_sentence()



