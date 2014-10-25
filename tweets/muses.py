'''
.. py:module:: muses
    :platform: Unix
    
Muses for tweets. 

Muse is an object which on demand selects a new color code, which is then 
supposed to be framed in a context and converted into a tweet, if the name and 
framing are good enough. 

The muse can add other information for the framing 
and context generation algorithms, which are passed as is by the underlying
tweet-motor, i.e. one could create a muse which would name the selected color 
itself. However, as the underlying tweet-motor would not know how well the name
represents the color, it might produce undesired results as color code-name-framing
mappings' values would suffer if no ``muse_value``-key is added to the optional information. 
'''
import os
import sys
import random
import logging
from datetime import date, datetime, timedelta
from abc import ABCMeta


# In case we are not running these through Django, let module know
# the correct twitter app settings from TwatBot's settings file.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings
from django.utils import timezone

from reasoning import Reasoning
from new_age import NewAgePersonality
from models import EveryColorBotTweet
from models import Tweet

from tweets.utils import color

logger = logging.getLogger("tweets.default")

class Muse():
    """Abstract base class for muses.
    
    .. note::
        Create a child class and override ``inspire`` -method!
    """
    
    class Meta:
        __metaclass__ = ABCMeta
        
        
    def inspire(self):
        """Inspire tweets by giving a new color code and optionally other 
        information for the framing, etc.   
        
        .. note::
            Override in subclass!
        
        **Returns:**
            Dictionary, with at least ``color_code``-key which is a valid 
            color type. Other information can be anything the muse sees valid 
            for its purposes and should be passable to ``framing.frame`` as is.
        """
        color_code = self.select_color()
        return {'color_code': color_code}
        
    
    def select_color(self):
        """Select new color for the tweet.
        
        **Returns:**
            Color in accepted format.    
        """
        r, g, b = [random.randint(0, 255) for i in xrange(2)]
        return (r, g, b)
    
    # Internal copies
    __inspire = inspire
    __select_color = select_color
        
        
class EveryColorBotMuse(Muse):
    """Muse which inspires tweets by selecting colors from Everycolorbot's 
    tweets. 
    
    Does not pick same color twice, i.e. the results are saved to the
    database, and if run out of Everycolorbot tweet's does not inspire
    anymore.
    
    The saving of the tweeted status happens only after the tweet has been 
    successfully made by the core.
    """
    def __init__(self):
        self.color_threshold = 100.0
        
        
    def inspire(self):
        """Define a mood for the muse and select a color from the Everycolorbot's 
        tweets, which the bot has not tweeted yet.
        
        The color selected from choices is the closest to the current mood of the muse.
        
        **Returns:**
            Dict, which has ``color_code`` and ``everycolorbot_url`` -keys. If 
            all the colors has been tweeted, returns empty dict.
        """
        choices = self.get_choices()
        reasoning = Reasoning()
        if len(choices) == 0: 
            logger.info("EveryColorBotMuse could not find untweeted colors from its current choices. Tweet generation halted.")
            return reasoning 
        mood = NewAgePersonality().get_mood()
        aura = mood['aura_color']
        dist, choice = self.choose_color(aura, choices)
        if choice is None:
            logger.info("EveryColorBot could not find color close (closest:  ) enough its aura. Tweet generation halted".format(dist))
            return reasoning
        
        chtml = choice.color.html
        logger.info("EveryColorBotMuse choose color {} because it was closest to aura color {}, distance: {}".format(chtml, color.rgb2html(aura), dist))
        if not self.approve_color(chtml):  
            return reasoning
         
        chex = choice.color.hex
        d = {'color_code': chtml, 'retweet':True, 'retweet_url':choice.url,\
             'screen_name': 'everycolorbot', 'original_tweet': chex,\
             'muse': 'EveryColorBotMuse', 'values': {'muse': dist / 100},\
             'mood': mood,  'media': None}
        reasoning.set_attrs(d)      
        return reasoning
        
        
    def choose_color(self, aura_color, choices):
        """Choose EveryColorBotTweet which is closest to the given aura color."""
        color_list = []
        map(lambda ch: color_list.append(ch.color.html), choices)
        dist, color_code = color.get_closest(aura_color, color_list)
        choice = choices.filter(color__html = color_code)[0]
        if dist > self.color_threshold:
            return (0, None)
        return (dist, choice)
            
        
    def get_choices(self):
        """Get possible EveryColorBotTweet choices depending on the bot's 
        current activity.
        
        More recent tweets (based on database addition time) are emphasized.
        """
        # TODO: make activity depend on time of day / week.
        activity = random.random()    
        if activity <= 0.10:
            logger.info("EveryColorBotMuse is lazily browsing all the untweeted tweets for perfect color.")
            choices = EveryColorBotTweet.objects.filter(tweeted=False)
        elif activity <= 0.25:
            logger.info("EveryColorBotMuse is browsing all the untweeted tweets added in last 7 days for perfect color.")
            choices = EveryColorBotTweet.objects.filter(tweeted = False, added__gte = timezone.now() - timedelta(7, 0))
        elif activity <= 0.5:
            logger.info("EveryColorBotMuse is browsing all the untweeted tweets added in last 2 days for perfect color.")
            choices = EveryColorBotTweet.objects.filter(tweeted = False, added__gte = timezone.now() - timedelta(2, 0))
        else: 
            logger.info("EveryColorBotMuse is on the fast lane, browsing only the tweets added in last 3 hours for perfect color.")
            choices = EveryColorBotTweet.objects.filter(tweeted = False, added__gte = timezone.now() - timedelta(0, 10800))
        return choices
    
    
    def approve_color(self, chtml):
        """Confirm that not too similar color has been tweeted in recent
        tweets."""
        last_tweets = Tweet.objects.all()[:5]
        for t in last_tweets:
            dist = color.ed(t.color_code, chtml)
            if  dist < 15:
                logger.info("Similar color {} (distance: {}) was Tweeted recently. Tweet generation halted.".format(t.color_code, dist))
                return False
        return True
            
        