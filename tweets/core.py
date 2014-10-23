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
import traceback

# In case we are not running these through Django, let module know
# the correct twitter app settings from TwatBot's settings file.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings
import tweepy

from muses import EveryColorBotMuse
from models import EveryColorBotTweet
from models import ReTweet, Tweet
from contexts import NewAgeContext
from color_semantics import ColorSemantics
from tweets.utils.color import create_temp_image

COLOR_SEMANTICS = ColorSemantics()
logger = logging.getLogger('tweets.core')

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
        self.threshold = 1.0
    
    
    def _get_new_tweet(self, inspiration):
        """Build a new tweet for the bot with given inspiration.
        
        **Returns:**
            Tuple (str, float, dict), (tweet, value, inspiration) where ``tweet`` 
            is the generated tweet, ``value`` is estimated value for the tweet 
            and ``inspiration`` is a dictionary returned by used muse.
        """
        semantics = self.color_semantics
        if 'color_semantics' in inspiration:
            semantics = inspiration['color_semantics']
        context = self.context    
        if 'context' in inspiration:
            context = inspiration['context'] 
        inspiration['context'] = context.__class__.__name__
            
        names = semantics.name_color(k = 1, **inspiration)
        
        tweets = []
        for name, code, distance in names: 
            distance = distance / 100
            t = context.build_tweet(color_name = name, wisdom_count = 10,  **inspiration)
            if t is not None:
                tweet, value = t
                value = 1.0 - value
                value += distance 
                tweets.append((tweet, value))
                inspiration['color_name'] = name
            
        if len(tweets) == 0:
            return None

        #TODO: See value of the tweet and the tweet memory and allow the tweet
        #if the stars are right.
        return (tweets[0][0], tweets[0][1], inspiration)
    
    
    def _tweet(self, tweet, img_name = None):
        """Tweet to the twitter.
        
        .. warning:: 
            Don't use this method directly as the sent tweets are not stored in
            the bot's memory.
        
        **Returns:**
            True if the tweet was send successfully, False otherwise.
        """
        if DEBUG: 
            logger.info("DEBUG mode on, choosing not to tweet.")
            return False
            
        try:
            auth = tweepy.OAuthHandler(self.tak, self.tas)
            auth.set_access_token(self.tat, self.tats)
            api = tweepy.API(auth)
            if img_name:
                api.update_with_media(filename = img_name,status = tweet)
            else:
                api.update_status(status = tweet)
        except Exception:
            e = traceback.format_exc()
            logger.error("Could not tweet to Twitter. Error: {}".format(e))
            return False
        
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
        inspiration = self.muse.inspire()
        if not inspiration: return {'tweet': "", 'sended': False, 'value': 0.0, 'metadata': {}}    
        ret = self._get_new_tweet(inspiration)
        rdict = {'tweet': "", 'sended': False, 'metadata': {}}
        if ret is None: return rdict
        tweet, value, reasoning = ret
        if send_to_twitter:
            logger.info('Build tweet: "{}" with value: {}'.format(tweet, value))
        tweeted = False
        if value < self.threshold:
            if send_to_twitter:
                logger.info("Value of the tweet was below threshold ({}). Trying to tweet it.".format(self.threshold))          
                tmp_img = create_temp_image((480, 360), reasoning['color_code'])
                tweeted = self._tweet(tweet, img_name = tmp_img.name)
                tmp_img.close()
            if tweeted:
                self._save_to_db(tweet, value, reasoning)
           
        rdict['tweet'] = tweet
        rdict['sended'] = tweeted
        rdict['value'] = value
        rdict['metadata'] = reasoning
        return rdict
    
    
    def _save_to_db(self, tweet, value, reasoning):
        """Save the tweet to db."""
        logger.info("Tweet was send succesfully. Saving the tweet to database.")
        context = reasoning['context']
        muse = reasoning['muse']   
        color_code = reasoning['color_code']
        color_name = reasoning['color_name']

        twinst = Tweet(message = tweet, value = value, muse = muse,\
                     context = context, color_code = color_code,\
                     color_name = color_name)
        twinst.save()
        
        retweet = reasoning['retweet'] if 'retweet' in reasoning else False
        if retweet:
            screen_name = reasoning['screen_name']
            if screen_name == 'everycolorbot':
                inst = EveryColorBotTweet.objects.get_or_none(url = reasoning['url'])
                if inst:
                    inst.tweeted = True
                    inst.save()
                    
            reinst = ReTweet(tweet_url = reasoning['url'],\
                             screen_name = screen_name, tweet = twinst)
            reinst.save()
 
    
TWEET_CORE = TweetCore()
        
        