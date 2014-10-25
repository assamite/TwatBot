'''
.. py:module:: reasoning
    :platform: Unix
    
Reasoning object for the tweets.
'''
import logging
import traceback

logger = logging.getLogger('tweets.default')

class Reasoning():
    """Reasoning for the tweets.
    
    Class is used to hold information about the tweet's construction, and contains 
    few utility functions for convenience.
    
    After the tweet has been constructed, the class should hold at least 
    following attributes:
    
    * color_code (str or unicode): color of the tweet in html-format.
    * color_name (str or unicode: name constructed for the color code
    * tweet (str or unicode): text of the tweet 
    * retweet (bool): is the tweet a retweet 
    * retweet_url (str of unicode): URL for the retweet (if any)
    * muse (str or unicode): class name of the used muse
    * context (str or unicode): class name of the used context
    * values (dict): dictionary of the appreciation values generated during the 
    tweet's construction
     
    """
    def __init__(self, **kwargs):
        self.color_code = ""
        self.color_name = ""
        self.tweet = ""
        self.retweet = False
        self.retweet_url = ""
        self.muse = ""
        self.context = ""
        self.values = {}
        
        for k, v in kwargs.items():
            setattr(self, k, v)
            
            
    def set_attr(self, name, value):
        """Define new or change old attribute value.
        
        **Args:**
            | name (str): Name of the attribute
            | value: New attribute value
        """
        setattr(self, name, value)
                
            
    def save(self):
        """Save tweet to database."""
        from models import EveryColorBotTweet, Tweet, ReTweet
        
        logger.info("Saving the tweet to database.")
        try: 
            twinst = Tweet(message = self.tweet, value = self.value, muse = self.muse,\
                         context = self.context, color_code = self.color_code,\
                         color_name = self.color_name)
            twinst.save()
            
            if self.retweet:
                screen_name = self.screen_name
                if screen_name == 'everycolorbot':
                    inst = EveryColorBotTweet.objects.get_or_none(url = self.retweet_url)
                    if inst:
                        inst.tweeted = True
                        inst.save()
                        
                reinst = ReTweet(tweet_url = self.retweet_url,\
                                 screen_name = screen_name, tweet = twinst)
                reinst.save()
        except Exception:
            e = traceback.format_exc()
            logger.error("Could not save tweet to database, because of error: {}".format(e))
    
