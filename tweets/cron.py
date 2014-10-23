'''Cron jobs from django-cron.
'''
import sys
import os 

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'

import logging
import traceback
from django.conf import settings
from django_cron import CronJobBase, Schedule
import tweepy

from core import TWEET_CORE
from models import EveryColorBotTweet, Color, Tweet
from tweets.utils import color as cu

logger = logging.getLogger('django.cron')

class TwitterAccountListener(CronJobBase):
    RUN_EVERY_MINS = 30
    RETRY_AFTER_FAILURE_MINS = 5
    screen_name = "everycolorbot"
    _tak = settings.TWITTER_API_KEY
    _tas = settings.TWITTER_API_SECRET
    _tat = settings.TWITTER_ACCESS_TOKEN
    _tats = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = "tweets.TwitterAccountListener"
     
    def do(self): 
        logger.info("Initiating cronjob: {}".format(self.code)) 
        try:
            auth = tweepy.OAuthHandler(self._tak, self._tas)
            auth.set_access_token(self._tat, self._tats)
            api = tweepy.API(auth)
            user_timeline = api.user_timeline(screen_name = self.screen_name)
        except Exception:
            e = traceback.format_exc()
            logger.error("Could not get timeline for user {}. Error: {}".format(self.screen_name, e))
            return False
        
        not_seen = []
        for t in user_timeline:
            if t.author.screen_name == self.screen_name:
                chex, url = t.text.split() 
                tweet_id = t.id_str
                if EveryColorBotTweet.objects.get_or_none(url = url) is None:
                    R, G, B = cu.hex2rgb(chex)
                    html = cu.rgb2html((R, G, B))
                    l, a, b = (cu._2lab((R, G, B))).get_value_tuple()
                    color_inst = Color.objects.get_or_none(html = html)                                                   
                    if color_inst is None:
                        color_inst = Color(html = html, hex = chex, rgb_r = R, rgb_g = G, rgb_b = B, l = l, a = a, b = b)
                        color_inst.save()
    
                    not_seen.append({'color_code': chex, 'everycolorbot_url': url})
                    logger.info("Adding {} {} into EveryColorBotTweet-table".format(chex, url))
                    instance = EveryColorBotTweet(color = color_inst, url = url, tweeted = False, tweet_id = tweet_id)
                    instance.save()
                    

class NewAgeTweeter(CronJobBase):
    RUN_EVERY_MINS = 30
    RETRY_AFTER_FAILURE_MINS = 5
    _tak = settings.TWITTER_API_KEY
    _tas = settings.TWITTER_API_SECRET
    _tat = settings.TWITTER_ACCESS_TOKEN
    _tats = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = "tweets.NewAgeTweeter"
     
    def do(self): 
        logger.info("Initiating cronjob: {}".format(self.code)) 
           
        try:
            TWEET_CORE.tweet(send_to_twitter = True)
        except:
            return False
        
        return True
                
                
class HomeTimelineCleaner(CronJobBase):
    RUN_EVERY_MINS = 30
    RETRY_AFTER_FAILURE_MINS = 5
    _tak = settings.TWITTER_API_KEY
    _tas = settings.TWITTER_API_SECRET
    _tat = settings.TWITTER_ACCESS_TOKEN
    _tats = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = "tweets.HomeTimelineCleaner"
    
    def do(self):
        logger.info("Initiating cronjob: {}".format(self.code)) 
        try:
            auth = tweepy.OAuthHandler(self._tak, self._tas)
            auth.set_access_token(self._tat, self._tats)
            api = tweepy.API(auth)
            timeline = api.home_timeline()
        except Exception:
            e = traceback.format_exc()
            logger.error("Could not get home timeline. Error: {}".format(self.screen_name, e))
            return False
        
        for t in timeline:
            msg = t.text
            if msg.startswith('RT @everycolorbot'):
                chex = msg.split()[2].strip("\"")
                evcinst = EveryColorBotTweet.objects.get_or_none(color__hex = chex)
                if evcinst is not None:
                    evcinst.tweeted = True
                    evcinst.save()
            inst = Tweet.objects.get_or_none(message = msg)
            if inst is None:
                logger.info('Cronjob encountered unsaved tweet: "{}" Saving it to database.'.format(msg))
                inst = Tweet(color_code = chex, message = msg) 
                inst.save()
                
            
                