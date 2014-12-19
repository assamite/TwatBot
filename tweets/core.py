"""
.. py:module:: core
    :platform: Unix
    
Core of the color tweets. 

Class TweetCore defined in the module glues muses, framing contexts and other 
tweet related functionalities together and allows the constructed messages to be 
tweeted, if the stars are right and everything is well in the kingdom.
"""
import os
import sys
import math
import logging
import operator
import traceback

# In case we are not running these through Django, let module know
# the correct twitter app settings from TwatBot's settings file.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings
import tweepy

from muses import EveryColorBotMuse
from contexts import NewAgeContext
from color_semantics import ColorSemantics

COLOR_SEMANTICS = ColorSemantics()
logger = logging.getLogger('tweets.default')

DEBUG = False

class TweetCore():
    """Core of the color tweets.
    
    Class attachs muses and framing contexts together to single functionality.
    
    .. note::
        At the moment class is quite deterministic. It should not be somewhere 
        in the future.
    """
    def __init__(self, color_semantics = COLOR_SEMANTICS, muse = EveryColorBotMuse(), context = NewAgeContext()):      
        self.tak = settings.TWITTER_API_KEY
        self.tas = settings.TWITTER_API_SECRET
        self.tat = settings.TWITTER_ACCESS_TOKEN
        self.tats = settings.TWITTER_ACCESS_TOKEN_SECRET
        self.color_semantics = color_semantics
        self.muse = muse
        self.context = context
        self.threshold = 0.55
    
    
    def _get_new_tweet(self, reasoning):
        """Build a new tweet for the bot with given reasoning.
        
        Builds new tweet by calling separately appropriate color and context 
        objects. The generated tweet is stored into the given :py:class:`tweets.Reasoning`
        object's tweet-value. After successful tweet generation the ``reasoning`` 
        also holds other information accumulated during the generation process
        
        :param reasoning: Reasoning object where the color code has been set
        :type reasoning: :py:class:`tweets.Reasoning`
        :returns: bool -- True is the building was successful, False otherwise.
        """
        if reasoning.color_semantics is None:
            reasoning.set_attr('color_semantics', self.color_semantics)
        semantics = reasoning.color_semantics  
        if reasoning.context is None:
            reasoning.set_attr('context', self.context)
        context = reasoning.context
            
        ret = semantics.name_color(reasoning)
        if not ret: return False    
        
        ret = context.build_tweet(reasoning)
        if not ret: return False    
        
        self._calculate_appreciation(reasoning)  
        return True      
    
    
    def _calculate_appreciation(self, reasoning):
        appr = 0.0
        values_count = len(reasoning.values.keys())
        for k, v in reasoning.values.items():
            appr += v ** 2
        
        appr = math.sqrt(appr)
        appr /= math.sqrt(values_count)
        reasoning.set_attr('appreciation', appr)
             
    
    def _tweet(self, tweet, img_name = None):
        '''Tweet to the twitter.
        
        .. warning:: 
            Don't use this method directly as the sent tweets are not stored in
            the bot's memory.
        
        :returns: tuple -- (bool, str), where bool is True if the tweet was send,
        and False otherwise. str contains the actual tweet returned by Twitter,
        it can be altered from the given tweet by, e.g. adding short URL for the
        given image.
        '''
        if DEBUG: 
            logger.info("DEBUG mode on, choosing not to tweet.")
            return (True, tweet)
            
        try:
            auth = tweepy.OAuthHandler(self.tak, self.tas)
            auth.set_access_token(self.tat, self.tats)
            api = tweepy.API(auth)
            if img_name:
                ret = api.update_with_media(filename = img_name,status = tweet)
                tweet = ret.text
            else:
                api.update_status(status = tweet)
        except Exception:
            e = traceback.format_exc()
            logger.error("Could not tweet to Twitter. Error: {}".format(e))
            return (False, "")
        
        return (True, tweet)
    
    
    def tweet(self, send_to_twitter = False, reasoning = None):
        '''Build a tweet for the bot and optionally send it to twitter and store it to bot's memory.
        
        :param send_to_twitter: Send succesfully generated, and enough appreciated tweet to Twitter
        :type send_to_twitter: bool
        :param reasoning: Optional, custom reasoning for this tweet, should containt at least key *color_code*.
        :type reasoning: :py:class:`tweets.Reasoning`
        :returns: :py:class:`.tweets.Reasoning` -- Reasoning object containing information about the tweet generation process
        '''  
        if reasoning is None:
            reasoning = self.muse.inspire()
        if reasoning.color_code == '': 
            return reasoning
        ret = self._get_new_tweet(reasoning)
        if not ret:
            return reasoning
        logger.info('Built tweet: "{}" with value: {}'.format(reasoning.tweet, reasoning.appreciation))
        tweeted = False
        if reasoning.appreciation < self.threshold and send_to_twitter:
            logger.info("Value of the tweet was below threshold ({}). Trying to tweet it.".format(self.threshold))     
            tweeted, tweet = self._tweet(reasoning.tweet, img_name = reasoning.media.name)
            reasoning.set_attr('tweet', tweet)
            reasoning.set_attr('tweeted', tweeted)
            if tweeted:
                reasoning.save()
                
        return reasoning


    
TWEET_CORE = TweetCore()
        
        