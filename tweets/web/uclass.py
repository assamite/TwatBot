'''
.. py:module:: uclass
    :platform: Unix
    
Different text classification techniques using `uClassify <http://www.uclassify.com>`_.

For each of the classifiers, the `texts` argument is a list of strings, which
are classified separately.
'''
import sys, os, logging
from uclassify import uclassify as uc
import unidecode

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings

logger = logging.getLogger('tweets.default')


def _parse(texts):
    t = []
    for txt in texts:
        t.append(unidecode.unidecode(txt))
    return t

def sentiment(texts):
    '''uClassify Sentiment-classifier.'''
    cl = uc()
    cl.setReadApiKey(settings.UCLASSIFY_API_READ)
    ret = cl.classify(_parse(texts), classifierName = 'Sentiment', username = 'uClassify')
    return ret
    
    
def mood(texts):
    '''uClassify Mood-classifier.
    
    :returns: tuple -- certainty, happiness percent
    '''
    cl = uc()
    cl.setReadApiKey(settings.UCLASSIFY_API_READ)
    ret = cl.classify(_parse(texts), classifierName = 'Mood', username = 'prfekt')
    return ret


def values(texts):
    '''uClassify Values-classifier.'''
    cl = uc()
    cl.setReadApiKey(settings.UCLASSIFY_API_READ)
    ret = cl.classify(_parse(texts), classifierName = 'Values', username = 'prfekt')
    return ret


def mb_judging(texts):
    '''uClassify Myers Briggs Judging Function-classifier.
    
    Determines the Thinking/Feeling dimension of the personality type according to Myers-Briggs personality model.
    '''
    cl = uc()
    cl.setReadApiKey(settings.UCLASSIFY_API_READ)
    ret = cl.classify(_parse(texts), classifierName = 'Myers Briggs Judging Function', username = 'prfekt')
    return ret


def mb_attitude(texts):
    '''uClassify Myers Briggs Attitude-classifier.
    
    Analyzes the Extraversion/Introversion dimension of the personality type according to Myers-Briggs personality model.
    '''
    cl = uc()
    cl.setReadApiKey(settings.UCLASSIFY_API_READ)
    ret = cl.classify(_parse(texts), classifierName = 'Myers Briggs Attitude', username = 'prfekt')
    return ret


def mb_perceiving(texts):
    '''uClassify Myers Briggs Perceiving Function-classifier.
    
    Determines the Sensing/iNtuition dimension of the personality type according to Myers-Briggs personality model.
    '''
    cl = uc()
    cl.setReadApiKey(settings.UCLASSIFY_API_READ)
    ret = cl.classify(_parse(texts), classifierName = 'Myers Briggs Perceiving Function', username = 'prfekt')
    return ret


def mb_lifestyle(texts):
    '''uClassify Myers Briggs Lifestyle-classifier.
    
    Determines the Judging/Perceiving dimension of the personality type according to Myers-Briggs personality model.
    '''
    cl = uc()
    cl.setReadApiKey(settings.UCLASSIFY_API_READ)
    ret = cl.classify(_parse(texts), classifierName = 'Myers Briggs Lifestyle', username = 'prfekt')
    return ret

    
