'''
.. py:module:: contexts
    :platform: Unix
    
Contexts for framing the tweets. 
'''
import sys
import os
from abc import ABCMeta
import urllib2
import operator
from subprocess import Popen, PIPE

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings

from text_utils import prettify_sentence


class Context():
    """Abstract base class for contexts.
    
    .. note::
        Create a child class of this and override ``build_tweet`` -method.
    """
    
    class Meta:
        __metaclass__ = ABCMeta
     
    def build_tweet(self, color_code, color_name, **kwargs):
        """Build tweet for color and its name.
        
        .. note:: 
            Override in child class!
        """
        return "%s %s" % (color_code, color_name)
    
    
class TextContext(Context):
    """Basic text context. Nothing fancy here, yet."""
    
    def build_tweet(self, color_name, **kwargs):
        """Build tweet for color name.
        
        **Args:**
            | color_name (str): Human readable name for the color.
            | \**kwargs: Optional keyword arguments. Should have ``color_code`` -key and supports optionally at least ``everycolorbot_url`` which personalizes the response for Everycolorbot.
        
        **Returns:**
            str, tweet for the color code-name pair.
        """
        if "everycolorbot_url" in kwargs:
            return (".everycolorbot Gee, that's a nice color. I call it %s." % color_name, 0.0)
        return ("By hard thinking, I have come to the conclusion that color %s is called %s. #geniusatwork" % (color_code, color_name), 0.0)
    
    
    
class DCContext(Context):
    """Framing with 'random' new age liirumlaarum from Deepak Chopra.
    
    Uses `Wisdom of Deepak Chopra <www.wisdomofchopra.com>`_ as a help for framing. 
    
    .. warning::
        www.wisdomofchopra.com seems to be down.
    
    """
    url = 'http://www.wisdomofchopra.com/iframe.php'
    
    def __init__(self):
        from bs4 import BeautifulSoup as bs
        from nltk import word_tokenize, pos_tag
        from nltk.corpus import wordnet
        self.bs = bs
        self.tokenizer = word_tokenize
        self.pos_tag = pos_tag
        self.wordnet = wordnet
       
        
    def build_tweet(self, color_name, wisdom_count = 5, **kwargs):
        """Build tweet for color name.
        
        **Args:**
            | color_name (str): Human readable name for the color.
            | wisdom_count (int): How many different wisdoms are considered in order to find the best framing.
            | \**kwargs: Optional keyword arguments. Should have ``color_code`` -key and supports optionally at least ``everycolorbot_url`` which personalizes the response for Everycolorbot.
        
        **Returns:**
            str, tweet for the color code-name pair. If no tweet can be constructed (e.g. wisdomofchopra is down, no internet connection), 
            returns None.
        """
        wisdoms = self._get_wisdoms(color_name, wisdom_count = wisdom_count)
        if not wisdoms: return None 
        tweets = []
        for wis in wisdoms:
            tokenized = self.tokenizer(wis)
            tagged_wisdom = self.pos_tag(tokenized)
            ret = self._get_color_place(color_name, tagged_wisdom)
            if ret is not None:
                place, value = ret
                tweet = self._prettify_tweet(color_name, tokenized, place)
                tweets.append((tweet, value))
         
        if len(tweets) > 0:
            sorted_tweets = sorted(tweets, key = operator.itemgetter(1), reverse = True)    
            return sorted_tweets[0]
        else:
            return None
               
            
    def _get_wisdoms(self, color_name, wisdom_count = 3):
        """Get wisdoms from www.wisdomofchopra.com."""
        if type(wisdom_count) is not int or wisdom_count < 1:
            raise ValueError("wisdom_count must be positive integer.")
        
        wisdoms = []
        while len(wisdoms) < wisdom_count:
            try:
                resp = urllib2.urlopen(self.url).read()
                soup = self.bs(resp)
                wisdom = soup.find(id = "quote").find('h2').string
                wisdom = wisdom.strip().strip("\"")
                wisdom = wisdom if wisdom[-1] == "." else wisdom + "."
                if (len(wisdom) + len(color_name)) <= 120: 
                    wisdoms.append(wisdom)
            except:
                break # If there is no connection, etc.
            
        if len(wisdoms) == 0:
            return None
        else:
            return wisdoms
        
        
    def _get_color_place(self, color_name, tagged_wisdom):
        """Define place where to put the color name in the tagged sentence."""
        place_candidates = []
        for i in xrange(len(tagged_wisdom)):
            if tagged_wisdom[i][1][:2] == 'JJ':
                place_candidates.append(i)
            if tagged_wisdom[i][1][:2] == 'NN':
                if i == 0 or tagged_wisdom[i-i][1][:2] != 'NN':
                    place_candidates.append(i)
           
        if len(place_candidates) == 0: 
            return None   
        
        color_split = color_name.split()  
        color_synsets = []   
        for c in color_split:
            cs = self.wordnet.synsets(c)
            if len(cs) > 0:
                for synset in cs:
                    color_synsets.append(synset)
           
        if len(color_synsets) == None:
            return None
                  
        place_fits = {}
        for place in place_candidates:
            place_fits[place] = 0.0
            pos = self.wordnet.ADJ if tagged_wisdom[place][1][:2] == 'JJ' else self.wordnet.NOUN
            place_synsets = self.wordnet.synsets(tagged_wisdom[place][0], pos = pos)
            if len(place_synsets) > 0:
                for place_synset in place_synsets:
                    for csynset in color_synsets:
                        sim = place_synset.path_similarity(csynset)
                        if sim > place_fits[place]:
                            place_fits[place] = sim
        
        sorted_sim = sorted(place_fits.items(), key = operator.itemgetter(1), reverse = True)
        
        if sorted_sim[0][1] == 0.0:
            return None
        else:
            return sorted_sim[0]
        
    
    def _prettify_tweet(self, color_name, tokenized, place):
        if place == 0:
            tokenized[0] = tokenized[0][0].lower() + tokenized[0][1:]
            color_name = color_name[0].upper() + color_name[1:]
        
        words = tokenized[:place] + color_name.split() + tokenized[place:]
        return prettify_sentence(words)
            
        
    
class NewAgeContext(Context):
    """Framing with 'random' new age liirumlaarum.
    
    Bases on the work done by `Seb Pearce <http://sebpearce.com/bullshit/>`_, and needs 
    `Node.js <http://nodejs.org/>`_ to work.

    """
    def __init__(self):
        from bs4 import BeautifulSoup as bs
        from nltk import word_tokenize, pos_tag
        from nltk.corpus import wordnet
        self.bs = bs
        self.tokenizer = word_tokenize
        self.pos_tag = pos_tag
        self.wordnet = wordnet
       
        
    def build_tweet(self, color_name, wisdom_count = 3, **kwargs):
        """Build tweet for color name.
        
        **Args:**
            | color_name (str): Human readable name for the color.
            | wisdom_count (int): How many different wisdoms are considered in order to find the best framing.
            | \**kwargs: Optional keyword arguments. Should have ``color_code`` -key and supports optionally at least ``everycolorbot_url`` which personalizes the response for Everycolorbot.
        
        **Returns:**
            str, tweet for the color code-name pair. If no tweet can be constructed, returns None.
        """
        wisdoms = self._get_wisdoms(color_name, wisdom_count = wisdom_count)
        if not wisdoms: return None 
        tweets = []
        for wis in wisdoms:
            tokenized = self.tokenizer(wis)
            tagged_wisdom = self.pos_tag(tokenized)
            ret = self._get_color_place(color_name, tagged_wisdom)
            if ret is not None:
                place, value = ret
                tweet = self._prettify_tweet(color_name, tokenized, place)
                tweets.append((tweet, value))
         
        if len(tweets) > 0:
            sorted_tweets = sorted(tweets, key = operator.itemgetter(1), reverse = True)    
            return sorted_tweets[0]
        else:
            return None
               
            
    def _get_wisdoms(self, color_name, wisdom_count = 3):
        """Get wisdoms from www.wisdomofchopra.com."""
        if type(wisdom_count) is not int or wisdom_count < 1:
            raise ValueError("wisdom_count must be positive integer.")
        
        wisdoms = []
        js_path = os.path.join(settings.BASE_DIR, 'tweets', 'js', 'sentence.js')
        
        try:
            for i in xrange(wisdom_count):
                p = Popen(['node', js_path, "1"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
                output, err = p.communicate(b"input data that is passed to subprocess' stdin")
                wisdoms.append(output)
        except:
            return None
            
        return wisdoms
        
        
    def _get_color_place(self, color_name, tagged_wisdom):
        """Define place where to put the color name in the tagged sentence."""
        place_candidates = []
        for i in xrange(len(tagged_wisdom)):
            if tagged_wisdom[i][1][:2] == 'JJ':
                place_candidates.append(i)
            if tagged_wisdom[i][1][:2] == 'NN':
                if i == 0 or tagged_wisdom[i-i][1][:2] != 'NN':
                    place_candidates.append(i)
           
        if len(place_candidates) == 0: 
            return None   
        
        color_split = color_name.split()  
        color_synsets = []   
        for c in color_split:
            cs = self.wordnet.synsets(c)
            if len(cs) > 0:
                for synset in cs:
                    color_synsets.append(synset)
           
        if len(color_synsets) == None:
            return None
                  
        place_fits = {}
        for place in place_candidates:
            place_fits[place] = 0.0
            pos = self.wordnet.ADJ if tagged_wisdom[place][1][:2] == 'JJ' else self.wordnet.NOUN
            place_synsets = self.wordnet.synsets(tagged_wisdom[place][0], pos = pos)
            if len(place_synsets) > 0:
                for place_synset in place_synsets:
                    for csynset in color_synsets:
                        sim = place_synset.path_similarity(csynset)
                        if sim > place_fits[place]:
                            place_fits[place] = sim
        
        sorted_sim = sorted(place_fits.items(), key = operator.itemgetter(1), reverse = True)
        
        if sorted_sim[0][1] == 0.0:
            return None
        else:
            return sorted_sim[0]
        
    
    def _prettify_tweet(self, color_name, tokenized, place):
        if place == 0:
            tokenized[0] = tokenized[0][0].lower() + tokenized[0][1:]
            color_name = color_name[0].upper() + color_name[1:]
        
        words = tokenized[:place] + color_name.split() + tokenized[place:]
        return prettify_sentence(words)
            
                

