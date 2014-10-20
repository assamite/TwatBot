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
mappings' values would suffer if no ``value``-key is added to the optional information. 
'''
import os
import sys
import random
from abc import ABCMeta


# In case we are not running these through Django, let module know
# the correct twitter app settings from TwatBot's settings file.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings

from models import EveryColorBotTweet

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

    def inspire(self):
        """Select random color from the Everycolorbot's tweets, which TwatBot
        has not tweeted yet.
        
        **Returns:**
            Dict, which has ``color_code`` and ``everycolorbot_url`` -keys. If 
            all the colors has been tweeted, returns empty dict.
        """
        untweeted = EveryColorBotTweet.objects.filter(tweeted=False)
        if len(untweeted) == 0: 
            return {}
        choice = random.choice(untweeted)
        return {'color_code': choice.color.html, 'everycolorbot_url': choice.url}
        
        