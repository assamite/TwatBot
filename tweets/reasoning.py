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
    * tweeted (bool): Was the constructed tweet send to twitter
    * retweet (bool): is the tweet a retweet 
    * retweet_url (str or unicode): URL for the retweet (if any)
    * original_tweet (str or unicode): Original tweet if this is a retweet
    * muse: class instance of the used Muse
    * context: class instance of the used Context
    * color_semantics: class instance of the used ColorSemantics.
    * values (dict): dictionary of the appreciation values generated during the 
    tweet's construction.
     
    """
    def __init__(self, **kwargs):
        self.color_code = ""
        self.color_name = ""
        self.tweet = ""
        self.tweeted = False
        self.retweet = False
        self.retweet_url = ""
        self.original_tweet = ""
        self.muse_classname = ""
        self.color_semantics_classname = ""
        self.context_classname = ""
        self.values = {}
        self.media = None
        self.appreciation = 0.0
        
    
        
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    def __repr__(self):
        ret = ""
        for k, v in self.__dict__.items():
            ret = ret + k + ": " + str(v) + "\n"
        return ret 
            
            
    def set_attr(self, name, value):
        """Define new or change old attribute value. 
        
        Caller should take care of the possible conflicts when changing existing
        attribute values.
        
        **Args:**
            | name (str): Name of the attribute
            | value: New attribute value
        """
        setattr(self, name, value)
        if name == 'muse':
            setattr(self, 'muse_classname', value.__class__.__name__)
        if name == 'context':
            setattr(self, 'context_classname', value.__class__.__name__)
        if name == 'color_semantics':
            setattr(self, 'color_semantics_classname', value.__class__.__name__)
        
        
    def set_attrs(self, dict):
        """Define new or change old attribute values in a patch.
        
        Caller should take care of the possible conflicts when changing existing
        attribute values.
        
        **Args:**
            | dict (dict): Attribute mappings
        """
        for k, v in dict.items():
            self.set_attr(k, v)
                
            
    def save(self):
        """Save tweet to database."""
        from models import EveryColorBotTweet, Tweet, ReTweet
        
        logger.info("Saving the tweet to database.")
        try: 
            twinst = Tweet(message = self.tweet, value = self.value, muse = self.muse__classname,\
                         context = self.context__classname, color_code = self.color_code,\
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
    
