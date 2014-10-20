'''Cron jobs from django-cron.
'''
import sys
import os 

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'

import logging
from django.conf import settings
from django_cron import CronJobBase, Schedule
import tweepy

from core import TWEET_CORE
from models import EveryColorBotTweet

logger = logging.getLogger('tweets.cron')

class TwitterAccountListener(CronJobBase):
    RUN_EVERY_MINS = 30
    RETRY_AFTER_FAILURE_MINS = 5
    screen_name = "everycolorbot"
    _tat = settings.TWITTER_API_KEY
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
        except:
            return False
        
        not_seen = []
        for t in user_timeline:
            if t.screen_name == self.screen_name:
                color, url = t.text.split() 
                tweet_id = t.id_str
                if EveryColorBotTweet.objects.get_or_none(color=color) is None:
                    not_seen.append({'color_code': color, 'everycolorbot_url': url})
                    logger.info("Adding {} {} into EveryColorBotTweet-table".format(color, url))
                    instance = EveryColorBotTweet(color = color, url = url, tweeted = False, tweet_id = tweet_id)
                    instance.save()
                    

class NewAgeTweeter(CronJobBase):
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    _tat = settings.TWITTER_API_KEY
    _tas = settings.TWITTER_API_SECRET
    _tat = settings.TWITTER_ACCESS_TOKEN
    _tats = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = "tweets.NewAgeTweeter"
     
    def do(self): 
        logger.info("Initiating cronjob: {}".format(self.code)) 
           
        try:
            TWEET_CORE.tweet(True)
        except:
            return False
        
        return True
                