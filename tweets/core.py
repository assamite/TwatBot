'''
.. py:module:: core
    :platform: Unix
    
Core of the color tweets. 

Class TweetCore defined in the module glues muses, framing contexts and other 
tweet related stuff together and allows the constructed messages to be tweeted,
if the stars are right and everything is well in the kingdom.
'''
import os
import sys

import twitter

# In case we are not running these through Django, let module know
# the correct twitter app settings from TwatBot's settings file.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings

from muses import EveryColorBotMuse
from models import EveryColorBotTweet
from framing import frame

from color_semantics import ColorSemantics
COLOR_SEMANTICS = ColorSemantics()

class TweetCore():
    """Core of the color tweets.
    
    Class attachs muses and framing contexts together to single functionality.
    
    .. note::
        At the moment class is quite deterministic. It should not be somewhere 
        in the future.
    """
    def __init__(self):      
        self.tak = settings.TWITTER_API_KEY
        self.tas = settings.TWITTER_API_SECRET
        self.tat = settings.TWITTER_ACCESS_TOKEN
        self.tats = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    
    def _get_new_tweet(self):
        """Build a new tweet for the bot.
        
        **Returns:**
            Tuple (str, float, dict), (tweet, value, inspiration) where ``tweet`` 
            is the generated tweet, ``value`` is estimated value for the tweet 
            and ``inspiration`` is a dictionary returned by used muse.
        """
        muse = EveryColorBotMuse()
        inspiration = muse.inspire()
        tweet, value = frame(context = 'text', **inspiration)
        #TODO: See value of the tweet and the tweet memory and allow the tweet
        #if the stars are right.
        return (tweet, value, inspiration)
    
    
    def _tweet(self, tweet):
        """Tweet to the twitter.
        
        .. warning:: 
            Don't use this method directly as the sent tweets are not stored in
            the bot's memory.
        
        **Returns:**
            True if the tweet was send successfully, False otherwise.
        """
        try:
            self.api = twitter.Api(consumer_key = self.tak,
                                   consumer_secret = self.tas,
                                   access_token_key = self.tak,
                                   access_token_secret = self.tats)
            self.api.postUpdate(tweet)
        except:
            return False
        
        return True
    
    
    def tweet(self, send_to_twitter = False):
        """Build a tweet for the bot and optionally send it to twitter and store it to bot's memory.
        
        **Returns:**
            Tuple (str, bool), (tweet, sended), where ``tweet`` is the generated 
            tweet and ``sended`` is True if the tweet was send successfully, False otherwise.
        """
        tweet, value, inspiration = self._get_new_tweet()
        tweeted = False
        if send_to_twitter:
            tweeted = self._tweet(tweet)
        if tweeted:
            if 'everycolorbot_url' in inspiration:
                inst = EveryColorBotTweet.objects.get(url = inspiration['everycolorbot_url'])
                inst.tweeted = True
                inst.save()
                   
        return (tweet, tweeted)
    
TWEET_CORE = TweetCore()
        
        