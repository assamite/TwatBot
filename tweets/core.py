"""
.. py:module:: core
    :platform: Unix
    
Core of the color tweets. 

Class TweetCore defined in the module glues muses, framing contexts and other 
tweet related stuff together and allows the constructed messages to be tweeted,
if the stars are right and everything is well in the kingdom.
"""
import os
import sys
import logging

# In case we are not running these through Django, let module know
# the correct twitter app settings from TwatBot's settings file.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings
import tweepy

from muses import EveryColorBotMuse
from models import EveryColorBotTweet
from contexts import NewAgeContext
from color_semantics import ColorSemantics

COLOR_SEMANTICS = ColorSemantics()
logger = logging.getLogger('tweets.core')

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
    
    
    def _get_new_tweet(self, inspiration = None):
        """Build a new tweet for the bot with given inspiration
        
        **Returns:**
            Tuple (str, float, dict), (tweet, value, inspiration) where ``tweet`` 
            is the generated tweet, ``value`` is estimated value for the tweet 
            and ``inspiration`` is a dictionary returned by used muse.
        """
        if inspiration is None:
            inspiration = self.muse.inspire()
        semantics = self.color_semantics
        if 'color_semantics' in inspiration:
            semantics = inspiration['color_semantics']
        context = self.context    
        if 'context' in inspiration:
            context = inspiration['context'] 
            
        names = semantics.name_color(k = 1, **inspiration)[0]
        tweets = []
        for name in names: 
            t = context.build_tweet(name, **inspiration)
            if t is not None:
                tweets.append(t)
            
        if len(tweets) == 0:
            return None

        #TODO: See value of the tweet and the tweet memory and allow the tweet
        #if the stars are right.
        return (tweets[0][0], tweets[0][1], inspiration)
    
    
    def _tweet(self, tweet):
        """Tweet to the twitter.
        
        .. warning:: 
            Don't use this method directly as the sent tweets are not stored in
            the bot's memory.
        
        **Returns:**
            True if the tweet was send successfully, False otherwise.
        """
        try:
            auth = tweepy.OAuthHandler(self.tak, self.tas)
            auth.set_access_token(self.tat, self.tats)
            api = tweepy.API(auth)
            api.update_status(tweet)
        except:
            e = sys.exc_info()[0]
            logger.error("Could not tweet to twitter. Because of error: {}".format(e))
            return False
        
        logger.info("Tweet was send succesfully. Saving the tweet to database.")
        return True
    
    
    def tweet(self, send_to_twitter = False, inspiration = None):
        """Build a tweet for the bot and optionally send it to twitter and store it to bot's memory.
        
        **Args:**
            | send_to_twitter (bool): Is succesfully generated and enough appreciation gained tweet send to twitter.
            | inspiration (dict): Optional, given inspiration for this tweet, should contain at least 'color_code'-key. If no inspiration is given, the standard muse is used to provide inspiration.
        
        **Returns:**
            Dictionary, with following keys: tweet, sended, value, metadata. 
            Tweet is the generated tweet and sended is True if the tweet was send 
            successfully, False otherwise. Value is estimated appreciation of the
            code-name-tweet mapping. Metadata contains other information of the 
            tweet generation process, including used color code and name, etc.
            
            If no tweet could be generated, then returns empty string as tweet. 
        """
        ret = self._get_new_tweet(inspiration)
        rdict = {'tweet': "", 'sended': False, 'metadata': {}}
        if ret is None: return rdict
        tweet, value, reasoning = self._get_new_tweet(inspiration)
        logger.info('Build tweet: "{}" with value: {}'.format(tweet, value))
        tweeted = False
        if send_to_twitter:
            tweeted = self._tweet(tweet)
        if tweeted:
            if 'everycolorbot_url' in inspiration:
                inst = EveryColorBotTweet.objects.get(url = inspiration['everycolorbot_url'])
                inst.tweeted = True
                inst.save()
           
        rdict['tweet'] = tweet
        rdict['sended'] = tweeted
        rdict['value'] = value
        rdict['metadata'] = reasoning
    
        return rdict
    
TWEET_CORE = TweetCore()
        
        