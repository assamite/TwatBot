'''
.. py:module:: therex
    :platform: Unix
    
Interface for accessing `Thesaurus Rex <http://ngrams.ucd.ie/therex2/>`_. 
'''
import urllib2
import logging
import traceback
import operator
from unidecode import unidecode
from xml.etree import ElementTree as ET

logger = logging.getLogger('tweets.default')
THESAURUS_REX_MEMBER_URL = "http://ngrams.ucd.ie/therex2/common-nouns/member.action?member={0}&kw={0}&needDisamb=true&xml=true"
THESAURUS_REX_SHARE_URL = "http://ngrams.ucd.ie/therex2/common-nouns/share.action?word1={0}&word2={1}&xml=true"

def _build_url(word1, word2 = None):
    # Convert unicode strings to normal ones as URL cannot have unicode chars.
    if type(word1) is unicode:
        word1 = unidecode(word1)
    if type(word2) is unicode:
        word2 = unidecode(word2)
    
    if word2 is None:
        return THESAURUS_REX_MEMBER_URL.format(word1)
    else:
        return THESAURUS_REX_SHARE_URL.format(word1, word2)
    
    
def _get_dict(element_tree, word1, word2):
    d = {}
    if word2 is None:
        d['Categories'] = []
        d['Modifiers'] = []
        d['CategoryHeads'] = []
        for e in element_tree[0]:
            d['Categories'].append((e.text.strip(), int(e.attrib['weight'])))
        for e in element_tree[1]:
            d['Modifiers'].append((e.text.strip(), int(e.attrib['weight'])))
        for e in element_tree[2]:
            d['CategoryHeads'].append((e.text.strip(), int(e.attrib['weight'])))       
    else:
        d['Categories'] = []
        d[u'{0}->{1}'.format(word1, word2)] = []
        d[u'{1}->{0}'.format(word2, word1)] = []
        for e in element_tree[0]:
            d['Categories'].append((e.text.strip(), int(e.attrib['weight'])))
        for e in element_tree[1]:
            d[u'{0}->{1}'.format(word1, word2)].append((e.text.strip(), int(e.attrib['weight'])))
        for e in element_tree[2]:
            d[u'{1}->{0}'.format(word2, word1)].append((e.text.strip(), int(e.attrib['weight'])))  
            
    for k in d:
        d[k] = sorted(d[k], key = operator.itemgetter(1), reverse = True)
        
    return d
        

def categories(word1, word2 = None):
    '''Thesaurus rex categories for single word or categories shared by two words.
    
    Does a web query to http://ngrams.ucd.ie/therex2/
    
    **Attrs:**
        | word1 (str or unicode): first word
        | word2 (str or unicode): optional, second word for the shared category query
    
    **Returns:**
        dict, xml response from Thesaurus Rex converted into dictionary, or None 
        if the web query was not successful. Dictionary values are lists ordered
        by weight of the category. Dictionary keys depend on the amount of words 
        used in the query.
    '''
    if type(word1) not in (str, unicode):
        raise TypeError("word1 must be str or unicode. Got {}".format(type(word1)))
    if word2 is not None and type(word2) not in (str, unicode):
        raise TypeError("If specified, word2 must be str or unicode. Got {}".format(type(word2)))
    
    try:
        response = urllib2.urlopen(_build_url(word1, word2)).read()
        et = ET.fromstring(response)
    except Exception:
        e = traceback.format_exc()
        logger.error("Could not get Thesaurus Rex categories, because of error: {}".format(e))
        return None 
    return _get_dict(et, word1, word2)
