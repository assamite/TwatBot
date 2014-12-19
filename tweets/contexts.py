'''
.. py:module:: contexts
    :platform: Unix
    
Contexts for framing the tweets. 
'''
import sys
import os
from abc import ABCMeta
import time
import json
import urllib
import urllib2
import operator
import logging
import traceback
import datetime
from random import choice
from PIL import Image
from pattern.en import parse
from collections import Counter

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings

from tweets.web import flickr, tinyurl
from tweets.models import Tweet, FlickrTweetImage, URLTweetImage
from tweets.utils import text, image, color as cu
from tweets.sentence import generate_text
from tweets.new_age import get_closest_mood_color
import interjections


logger = logging.getLogger("tweets.default")

class ABCContext():
    """Abstract base class for contexts.
    
    .. note::
        Create a child class of this and override :py:func:`build_tweet`.
    """
    
    class Meta:
        __metaclass__ = ABCMeta
     
    def build_tweet(self, color_code, color_name, **kwargs):
        """Build tweet for color and its name.
        
        .. note:: 
            Override in child class!
        """
        return "%s %s" % (color_code, color_name)
    
    
class TextContext(ABCContext):
    """Basic text context. Nothing fancy here, yet."""
    
    def build_tweet(self, color_name, **kwargs):
        """Build tweet for color name.
        
        **Args:**
            | color_name (str): Human readable name for the color.
            | \**kwargs: Optional keyword arguments. Should have ``color_code`` -key and supports optionally at least ``everycolorbot_url`` which personalizes the response for Everycolorbot.
        
        **Returns:**
            str, tweet for the color code-name pair.
        """
        if "everycolorbot_url" in kwargs:
            return (".everycolorbot Gee, that's a nice color. I call it %s." % color_name, 0.0)
        return ("By hard thinking, I have come to the conclusion that color %s is called %s. #geniusatwork" % (color_code, color_name), 0.0)
    
    
    
class DCContext(ABCContext):
    """Framing with 'random' new age liirumlaarum from Deepak Chopra.
    
    Uses `Wisdom of Deepak Chopra <www.wisdomofchopra.com>`_ as a help for framing. 
    
    .. warning::
        www.wisdomofchopra.com seems to be down.
    
    """
    url = 'http://www.wisdomofchopra.com/iframe.php'
    
    def __init__(self):
        from bs4 import BeautifulSoup as bs
        from nltk import word_tokenize, pos_tag
        from nltk.corpus import wordnet
        self.bs = bs
        self.tokenizer = word_tokenize
        self.pos_tag = pos_tag
        self.wordnet = wordnet
       
        
    def build_tweet(self, color_name, wisdom_count = 5, **kwargs):
        """Build tweet for color name.
        
        **Args:**
            | color_name (str): Human readable name for the color.
            | wisdom_count (int): How many different wisdoms are considered in order to find the best framing.
            | \**kwargs: Optional keyword arguments. Should have ``color_code`` -key and supports optionally at least ``retweet``.
        
        **Returns:**
            str, tweet for the color code-name pair. If no tweet can be constructed (e.g. wisdomofchopra is down, no internet connection), 
            returns None.
        """
        for k, v in kwargs.items():
            print k, v
        
        wisdoms = self._get_wisdoms(color_name, wisdom_count = wisdom_count)
        if not wisdoms: return None 
        tweets = []
        for wis in wisdoms:
            tokenized = self.tokenizer(wis)
            tagged_wisdom = self.pos_tag(tokenized)
            ret = self._get_color_place(color_name, tagged_wisdom)
            if ret is not None:
                place, value = ret
                tweet = self._prettify_tweet(color_name, tokenized, place)
                if 'retweet' in kwargs.keys(): 
                    tweet = "RT @{} {} {}".format(kwargs['screen_name'], kwargs['original_tweet'], tweet) 
                if len(tweet) <= 140:
                    tweets.append((tweet, value))
         
        if len(tweets) > 0:
            sorted_tweets = sorted(tweets, key = operator.itemgetter(1), reverse = True)    
            return sorted_tweets[0]
        else:
            return None
               
            
    def _get_wisdoms(self, color_name, wisdom_count = 3):
        """Get wisdoms from www.wisdomofchopra.com."""
        if type(wisdom_count) is not int or wisdom_count < 1:
            raise ValueError("wisdom_count must be positive integer.")
        
        wisdoms = []
        while len(wisdoms) < wisdom_count:
            try:
                resp = urllib2.urlopen(self.url).read()
                soup = self.bs(resp)
                wisdom = soup.find(id = "quote").find('h2').string
                wisdom = wisdom.strip().strip("\"")
                wisdom = wisdom if wisdom[-1] == "." else wisdom + "."
                if (len(wisdom) + len(color_name)) <= 120: 
                    wisdoms.append(wisdom)
            except:
                break # If there is no connection, etc.
            
        if len(wisdoms) == 0:
            return None
        else:
            return wisdoms
        
        
    def _get_color_place(self, color_name, tagged_wisdom):
        """Define place where to put the color name in the tagged sentence."""
        place_candidates = []
        for i in xrange(len(tagged_wisdom)):
            if tagged_wisdom[i][1][:2] == 'JJ':
                place_candidates.append(i)
            if tagged_wisdom[i][1][:2] == 'NN':
                if i == 0 or tagged_wisdom[i-i][1][:2] != 'NN':
                    place_candidates.append(i)
           
        if len(place_candidates) == 0: 
            return None   
        
        color_split = color_name.split()  
        color_synsets = []   
        for c in color_split:
            cs = self.wordnet.synsets(c)
            if len(cs) > 0:
                for synset in cs:
                    color_synsets.append(synset)
           
        if len(color_synsets) == None:
            return None
                  
        place_fits = {}
        for place in place_candidates:
            place_fits[place] = 0.0
            pos = self.wordnet.ADJ if tagged_wisdom[place][1][:2] == 'JJ' else self.wordnet.NOUN
            place_synsets = self.wordnet.synsets(tagged_wisdom[place][0], pos = pos)
            if len(place_synsets) > 0:
                for place_synset in place_synsets:
                    for csynset in color_synsets:
                        sim = place_synset.path_similarity(csynset)
                        if sim > place_fits[place]:
                            place_fits[place] = sim
        
        sorted_sim = sorted(place_fits.items(), key = operator.itemgetter(1), reverse = True)
        
        if sorted_sim[0][1] == 0.0:
            return None
        else:
            return sorted_sim[0]
        
    
    def _prettify_tweet(self, color_name, tokenized, place):
        if place == 0:
            tokenized[0] = tokenized[0][0].lower() + tokenized[0][1:]
            color_name = color_name[0].upper() + color_name[1:]
        
        words = tokenized[:place] + color_name.split() + tokenized[place:]
        return text.prettify(words)
            
        
    
class NewAgeContext(ABCContext):
    """Framing with 'random' new age liirumlaarum.
    
    Bases on the work done by `Seb Pearce <http://sebpearce.com/bullshit/>`_.

    """
    def __init__(self):
        from bs4 import BeautifulSoup as bs
        from nltk import word_tokenize, pos_tag
        from nltk.corpus import wordnet
        self.bs = bs
        self.tokenizer = word_tokenize
        self.pos_tag = pos_tag
        self.wordnet = wordnet
        self.tweet_similarity_threshold = 3
        self.memory_length = 15
        
    def build_tweet(self, reasoning):
        """Build tweet for color name.
        
        **Args:**
            | color_name (str): Human readable name for the color.
            | wisdom_count (int): How many different wisdoms are considered in order to find the best framing.
            | \**kwargs: Optional keyword arguments. Should have ``color_code`` -key and supports optionally at least ``everycolorbot_url`` which personalizes the response for Everycolorbot.
        
        **Returns:**
            str, tweet for the color code-name pair. If no tweet can be constructed, returns False.
        """
        color_name = reasoning.color_name
        wisdoms = self._get_wisdoms(color_name, wisdom_count = 10)
        if not wisdoms: 
            return None 
        tweets = []
        for wis in wisdoms:
            places, parsed_wisdom = self._get_color_places(color_name, wis)
            if places is not None:
                ret = self._evaluate_color_places(color_name, places, parsed_wisdom)
                if ret is not None:
                    place, value = ret
                    tweet = self._prettify_tweet(color_name, parsed_wisdom, place)
                    if reasoning.retweet: 
                        tweet = 'RT @{} "{}" {}'.format(reasoning.screen_name, reasoning.original_tweet, tweet) 
                    tweet_len = 118 if reasoning.media else 140   
                    if len(tweet) <= tweet_len:
                        tweets.append((tweet, 1.0 - value))
         
        if len(tweets) == 0:
            return False
                
        sorted_tweets = sorted(tweets, key = operator.itemgetter(1))  
        reasoning.set_attr('tweet', sorted_tweets[0][0])  
        reasoning.values['context'] = sorted_tweets[0][1]
        return True
               
            
    def _get_wisdoms(self, color_name, wisdom_count = 3):
        """Get wisdoms from sentence module"""
        if type(wisdom_count) is not int or wisdom_count < 1:
            raise ValueError("wisdom_count must be positive integer.")
        
        last_tweets = Tweet.objects.all()[:self.memory_length]
        wisdoms = []
        
        try:
            while len(wisdoms) < wisdom_count:
                wisdom = generate_text(1).strip()
                logger.debug("Generated wisdom: {}".format(wisdom))
                # Filter wisdoms too similar to latest tweets out
                if self._approve_wisdom(wisdom, last_tweets): 
                    wisdoms.append(wisdom.strip())
        except:
            return None
            
        return wisdoms
        
        
    def _get_color_places(self, color_name, sentence):
        """Define place where to put the color name in the sentence."""
        split_wisdom = sentence.split(" ")
        parsed_wisdom = []
        place_candidates = []
        removed = 0
        for i in xrange(len(split_wisdom)):
            if split_wisdom[i] == '<>':
                place_candidates.append(i - removed)
                removed += 1
            else:
                parsed_wisdom.append(split_wisdom[i])
           
        if len(place_candidates) == 0: 
            return None, parsed_wisdom
        
        return place_candidates, parsed_wisdom    
         
        
    def _evaluate_color_places(self, color_name, place_candidates, tagged_wisdom): 
        color_split = color_name.split()  
        color_synsets = []   
        for c in color_split:
            cs = self.wordnet.synsets(c)
            if len(cs) > 0:
                color_synsets.append(cs[0])
           
        if len(color_synsets) == None:
            return None
                  
        place_fits = {}
        for place in place_candidates:
            place_fits[place] = 0.0
            place_synsets = self.wordnet.synsets(tagged_wisdom[place])
            if len(place_synsets) > 0:
                for place_synset in place_synsets:
                    for csynset in color_synsets:
                        sim = place_synset.path_similarity(csynset)
                        if sim > place_fits[place]:
                            place_fits[place] = sim
        
        sorted_sim = sorted(place_fits.items(), key = operator.itemgetter(1), reverse = True)
        
        if sorted_sim[0][1] == 0.0:
            return None
        else:
            return sorted_sim[0]
        
    def _approve_wisdom(self, wisdom, last_tweets):
        for t in last_tweets:
            sw = text.same_words(wisdom, t.message)
            if sw > self.tweet_similarity_threshold:
                logger.debug("Discarding wisdom, because it was too similar ({}) with recent tweet: {}".format(sw, t.message))
                return False
        return True              
        
    
    def _prettify_tweet(self, color_name, tokenized, place):
        if place == 0:
            tokenized[0] = tokenized[0][0].lower() + tokenized[0][1:]
            color_name = color_name[0].upper() + color_name[1:]
            words = color_name.split() + tokenized[place:]
        else:
            words = tokenized[:place] + color_name.split() + tokenized[place:]
        return text.prettify(words)
            
                
class MonkeyImageContext(ABCContext):
    
    def build_tweet(self, reasoning):
        emotion = reasoning.reaction
        print emotion
        ret = interjections.get(emotion, settings.WORD2VEC_MODEL)
        if ret is None: return False
        interjection, base = ret
        url = tinyurl.get(reasoning.article['url'])
        photo = self.get_flickr_monkey_photo(emotion)
        #photo = False
        if not photo:
            print "plaa"
            photo_url = self.get_google_monkey_photo(emotion)
            if photo_url:
                photo = self.download_url_photo(photo_url)
        if not photo: return False
        
        color = get_closest_mood_color(emotion, settings.WORD2VEC_MODEL)
        color = cu.add_noise(color)
        color = list(color)
        color.append(192)
        color = tuple(color)
        photo = self.create_reaction_image(interjection, photo, color)
        if not photo: return False
        photo.interjection = base
        photo.save()
        save_path = os.path.join(settings.ROOT_DIR, photo.processed.path)
    
        tags = self._get_tags(reasoning.article['text'])
        stags = "#" + " #".join(tags) if len(tags) > 0 else '' 
        logger.info("Extracted tags '{}' for article '{}...'".format(stags, reasoning.article['url']))
        tweet = url + " " + stags
        while len(tweet) > 120:
            tweet = tweet.rsplit(" ", 1)[0]
            
        reasoning.set_attr('media', save_path)
        reasoning.set_attr('tweet_image', photo)
        reasoning.values['context'] = 1
        reasoning.set_attr('tweet', tweet)
        return True
        
        
    def get_flickr_monkey_photo(self, emotion):
        #search_text = "monkey {}".format(emotion)
        search_text = "cat {}".format(emotion)
        try:
            logging.info("Searching Flickr for images with text: '{}'".format(search_text))
            photos = flickr.photos_search(text = search_text)
        except:
            logger.error("Could not execute Flickr search because of error: {}".format(traceback.format_exc()))
            return False
        
        filtered_photos = []
        for p in photos:
            tags = p.tags.split()
            if 'cat' in tags and 'text' not in tags:
                filtered_photos.append(p)
                
        logger.info("Found {} images for the Flickr search: {}".format(len(filtered_photos), search_text))
        if len(filtered_photos) == 0:
            return False
        fphoto = choice(filtered_photos) 
        fti = FlickrTweetImage.objects.get_or_none(flickr_id = fphoto.id)
        if fti is None:
            fti = self.flickr_download_and_save(fphoto)
            
        return fti
    
    
    def get_google_monkey_photo(self, emotion):
        #search_text = 'animal monkey {}'.format(emotion)
        search_text = 'cat animal {}'.format(emotion)
        start = 0
        url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={}&rsz=8&start={}'
        current_url = url.format(search_text, start)
        found = False
        
        try:
            while found == False: 
                logger.info("Searching Google (start = {}) for images with text: '{}'".format(start, search_text))
                ret = urllib.urlopen(current_url).read()
                ret = json.loads(ret)
                status = ret['responseStatus']
                if  status != 200:
                    logger.info('Google image search returned response status {}, halting image search.'.format(status))
                    return False
                results = ret['responseData']['results']
                photo_url = self._filter_google_results(results)
                if photo_url:
                    found = True
                    continue
                start += 8
                current_url = url.format(search_text, start)
                if start > 60:
                    logger.info("Could not find suitable Google image in sufficient time. Halting image search.")
                    return False
                time.sleep(1)
        except:
            logger.error("Could not open url {} because of error: {}".format(current_url, traceback.format_exc()))
            return False
        
        return photo_url
    
    
    def download_url_photo(self, photo_url):   
        uti = URLTweetImage.objects.get_or_none(url = photo_url)
        if uti is not None:
            return uti
            
        photo_name = self._get_image_name(photo_url)  
        upload_path = os.path.join(settings.MEDIA_ROOT, settings.ORIGINAL_IMAGE_UPLOAD_PATH, photo_name)
        if not self._download_image(photo_url, upload_path):
            return False
        
        impath = os.path.join(settings.ORIGINAL_IMAGE_UPLOAD_PATH, photo_name)
        inst = URLTweetImage(original = impath, url = photo_url)  
        return inst
    
    
    def _filter_google_results(self, results):   
        if len(results) == 0:
            return False
        while len(results) > 0:
            photo = choice(results)
            content = photo['contentNoFormatting']
            print photo['contentNoFormatting'], photo['visibleUrl']
            if photo['visibleUrl'] == "www.shutterstock.com":
                pass         
            elif self.has_cat(content):
                logger.info("Found suitable image from Google with content: '{}'".format(content))
                return photo['unescapedUrl']
            results.remove(photo) 
        return False
        
        
    def has_cat(self, content):
        cats = ['cat', 'kitty', 'kitten', 'cats', 'kittens']
        ts = content.lower().split()
        for t in ts:
            if t in cats:
                return True
        return False
            
       
    def has_monkey(self, content):
        monkeys = ['ape', 'apes', 'monkey', 'monkeys', 'baboon', 'baboons', 'gorilla', 'gorillas', 'makaki', 'chimpanzee', 'chimp', 'chimps']
        ts = content.lower().split()
        for t in ts:
            if t in monkeys:
                return True
        return False
         
    
    def create_reaction_image(self, text, photo, color):
        try : 
            logging.info("Creating reaction image for {} ({}) with photo {}".format(text, str(color), photo.original.path))
            photo_name = photo.original.path.rsplit("/", 1)[1]
            photo_name = photo_name.rsplit(".", 1)[0] + ".png"
            save_path = os.path.join(settings.MEDIA_ROOT, settings.PROCESSED_IMAGE_UPLOAD_PATH, photo_name)
            img = Image.open(os.path.join(settings.MEDIA_ROOT, photo.original.path))
            if photo.__class__.__name__ == "FlickrTweetImage":
                caption = "Original image by {} @ Flickr".format(photo.flickr_user_name)       
                img = image.text2image(img, caption, background_color = (255, 255, 255, 100), font_color = (0, 0, 0, 255), font_size = 10, y_pos = 'down', x_pos = 'right', scale_font = False)
            img = image.text2image(img, text.upper(), font_color = color)
            img.save(save_path)
            pro_path = os.path.join(settings.PROCESSED_IMAGE_UPLOAD_PATH, photo_name)
            photo.processed = pro_path
            photo.save()
        except:
            logger.error("Could not create reaction image because of error: {}".format(traceback.format_exc()))
            return False
            
        return photo
        
        
    def flickr_download_and_save(self, photo):
        '''Download photo and save it locally.
        
            :param photo_id: Valid Flickr photo id
            :type photo_id: str
            :returns: int -- Ok = 0, failure > 0, check ``RETURN_CODES``
        '''

        image_urlz = photo.url_z
        image_name = self._get_image_name(image_urlz)
        abs_path = os.path.join(settings.MEDIA_ROOT, settings.ORIGINAL_IMAGE_UPLOAD_PATH, image_name) 
        upload_path = os.path.join(settings.ORIGINAL_IMAGE_UPLOAD_PATH, image_name)
        r1 = self._download_image(image_urlz, abs_path) 
        if not r1: return False
        
        instance = FlickrTweetImage(original = upload_path, \
                               flickr_id = photo.id, flickr_user_id = photo.owner,\
                               flickr_secret = photo.secret, flickr_farm = photo.farm,\
                               flickr_server = photo.server, title = photo.title,\
                               flickr_user_name = photo.owner_name,\
                               description = photo.description)
        
        instance.save()
        return instance

            
    def _download_image(self, url, upload_path):
        try: 
            logger.info("Downloading {} to {}".format(url, upload_path))
            urllib.urlretrieve(url, upload_path)      
        except Exception as e:
            logger.error("Image download failed: {}".format(traceback.print_exc(e)))
            return False
    
        # Check that downloaded content is indeed and image and not e.g.
        # 403 page. 
        try: 
            img = Image.open(upload_path)
        except Exception as e:
            if os.path.isfile(upload_path):
                logger.info("Deleting downloaded content from {} because of error: {}".format(upload_path, traceback.print_exc(e)))
                os.remove(upload_path)
            return False
        return True
        
            
    def _get_image_name(self, url): 
        photo_name = url.rsplit('/', 1)[1]
        if len(photo_name.split(".")) == 1:
            photo_name += '.jpg'
        
        import re
        time = datetime.datetime.now()
        time = str(time)
        time = re.sub(" ", "_", time)  
        time = re.sub(":", "", time)
        time = time[:17]
        photo_name = time + "_" + photo_name
        return photo_name
        
        
    def _get_tags(self, article):
        '''Get most promising tag words from the text.'''
        nnps = text.get_NNPs(article, True)
        a = 3 if len(nnps) > 3 else len(nnps)
        return [x[0] for x in  nnps[:a]]
            
        
            

