"""
.. py:module:: models
    :platform: Unix
    :synopsis: Django models for resources given on the course.

Django models to access and manipulate resources given on the course.
"""
from django.db import models
from django.conf import settings

from tweets.utils import color as cu

class GetOrNoneManager(models.Manager):
    """Manager which overrides Django's standard manager in all of the module's models.
    
    Adds utility functionality into the models.
    """
    def get_or_none(self, **kwargs):
        """Get model object or None is no object matching search criteria is found.
        """
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        

class Color(models.Model):
    """Color representations.
    
    **Fields:**
        | html (CharField): html style color definition
        | hex (CharField): hex style color definition
        | rgb_r (IntegerField): red value of the rgb-color space
        | rgb_g (IntegerField): green value of the rgb-color space
        | rgb_b (IntegerField): blue value of the rgb-color space
        | l (FloatField): lightness value of the Lab-color space
        | a (FloatField): a color-opponent value of the Lab-color space
        | b (FloatField): b color-opponent value of the Lab-color space
    """
    html = models.CharField(max_length = 7, unique = True)
    hex = models.CharField(max_length = 8, unique = True)
    rgb_r = models.IntegerField()
    rgb_g = models.IntegerField()
    rgb_b = models.IntegerField()
    l = models.FloatField()
    a = models.FloatField()
    b = models.FloatField()
    objects = GetOrNoneManager()
    
    @classmethod
    def create(cls, color):
        """Create model instance from color definition. 

        Other color definitions are converted from given color definition.
        
        **Args:**
            | color: color in any supported format. See supported formats from ``color_utils``-module.
            
        **Returns:**
            New model instance.         
        """
        crgb = cu._2rgb(color)
        chtml = cu.rgb2html(crgb)
        R, G, B = crgb
        chex = cu.rgb2hex(crgb)
        l, a, b = (cu._2lab(crgb)).get_value_tuple()
        return cls(html = chtml, hex = chex, rgb_r = R, rgb_g = G, rgb_b = B, l = l, a = a, b = b)   
        
    
    def __str__(self):
        return self.html
            
    class Meta:
        unique_together = ('rgb_r', 'rgb_g', 'rgb_b')


class BracketedColorBigram(models.Model):
    """Bracketed bigrams.
    
    **Fields:**
        | start_bracket (CharField): starting bracket, ``max_length = 40``.
        | w1 (CharField): first word, ``max_length = 40``.
        | w2 (CharField): second word, ``max_length = 40``.
        | end_bracket (CharField): ending bracket, ``max_length = 40``.
        | f (PositiveIntegerField): bigram's frequency
        
    Sample entries:
        
        =============    =======    ======    ===========    =
        start_bracket    w1         w2        end_bracket    f
        =============    =======    ======    ===========    =
        and              cheddar    cheese        ,          3477
        the              eye        candy         .          3476
        with             wood       wool         and         3448
        =============    =======    ======    ===========    =    
     
    """   
    start_bracket = models.CharField(max_length = 40)
    w1 = models.CharField(max_length = 40)
    w2 = models.CharField(max_length = 40)
    end_bracket = models.CharField(max_length = 40)
    f = models.PositiveIntegerField(default = 0)
    objects = GetOrNoneManager()
    
    def __str__(self):
        return " ".join((self.start_bracket, self.w1, self.w2, self.end_bracket, str(self.f)))
    
    class Meta:
        unique_together = ('start_bracket', 'w1', 'w2', 'end_bracket')
        ordering = ['-f']
    

class ColorMap(models.Model):
    """Color stereotype - color value pairs with base color names.
    
    **Fields:**
        | stereotype (CharField): Name of the color stereotype, ``max_length = 40``.
        | base_color (CharField): Base color name, ``max_length = 40``.
        | color (ForeignKey): Reference to ``Color``-model object.  
        
    Sample entries:
    
        ==========    ==========     ===
        stereotype    base_color     color.html
        ==========    ==========     ===
        acid          green          #B0BF1A
        absinthe      green          #7FDD4C
        acorn         brown          #7F6241
        ==========    ==========     ===    
         
    """ 
    stereotype = models.CharField(max_length = 40)
    base_color = models.CharField(max_length = 40, blank = True)
    color = models.ForeignKey(Color)
    objects = GetOrNoneManager()
    
    def __str__(self):
        return " ".join((self.stereotype, self.color, self.color.html))
    


class ColorUnigram(models.Model):
    """Color unigrams.
    
    **Fields:**
        | solid_compound (CharField): Solid compound of the unigram, ``max_length = 50``.
        | f (PositiveIntegerField): unigram's frequency
        
    Sample entries: 
    
        ===============    =
        solid_compound     f
        ===============    =
        aluminumleather    594
        amberbunny         240
        amberdawn          300
        ===============    =    
    """   
    solid_compound = models.CharField(max_length = 50)
    f = models.PositiveIntegerField(default = 0) 
    objects = GetOrNoneManager()
    
    def __str__(self):
        return " ".join((self.solid_compound, str(self.f)))
    
    class Meta:
        ordering = ['-f']
        
        
class ColorUnigramSplit(models.Model):
    """Splitted color unigrams.
    
    ``ColorUnigram`` -models ``solid_compound`` -fields that are splitted into 
    two words. Hopefully from somewhere it makes sense. 
    
    **Fields:**
        | w1 (CharField): First word of the unigram split, ``max_length = 40``.
        | w2 (CharField): Second word of the unigram split, ``max_length = 40``.
        | original (ForeignKey): Reference to original ``ColorUnigram`` -model instance.
        
    Sample entries (should look something like this): 
    
        ========    =======
        w1          w2  
        ========    =======
        aluminum    leather
        amber       bunny
        amber       dawn          
        ========    ======= 
    """   
    
    w1 = models.CharField(max_length = 40)
    w2 = models.CharField(max_length = 40)
    original = models.ForeignKey(ColorUnigram)
    objects = GetOrNoneManager()
    
    def __str__(self):
        return " ".join((self.w1, self.w2))
    
    class Meta:
        ordering = ['w1', 'w2']
        unique_together = ('w1', 'w2')


class EveryColorBotTweet(models.Model):
    """ URL's and colors for Everycolorbot's tweets.
    
    **Fields:**
        | added (DateTimeField): When the tweet was added to the database.
        | color (ForeignKey): Reference to ``Color``-model object.
        | tweeted (BooleanField): Has the color been used in a tweet.
        | url (URLField): URL for the tweet.
        | added (DateTimeField): Time when tweet was added to the database.
        | tweet_id (CharField): Tweet's id_str from Twitter
         
    Sample entries:    
     
        =========    =======    ===
        color.hex    tweeted    url
        =========    =======    ===
        0x634ef9     False      http://t.co/9OXdTPFOXK
        0x31a77c     False      http://t.co/99kdUpov9E
        0x98d3be     False      http://t.co/Os53Hh3qs7
        =========    =======    ===

    """ 
    url = models.URLField(unique = True)
    color = models.ForeignKey(Color)
    tweeted = models.BooleanField(default = False)
    added = models.DateTimeField(auto_now_add = True, null = True)
    tweet_id = models.CharField(max_length = 200, null = True)
    objects = GetOrNoneManager()
    
    def __str__(self):
        return " ".join((self.color.html, self.url))
    
    class Meta:
        ordering = ['-added', 'color', 'url', 'tweeted']
    

class PluralColorBigram(models.Model):
    """Plural color bigrams.
    
    **Fields:**
        | w1 (CharField): first word, ``max_length = 40``.
        | w2 (CharField): second word, ``max_length = 40``.
        | singular (CharField): singular of the second word, ``max_length = 40``.
        | f (PositiveIntegerField): bigram's frequency 
        
    Sample entries:
    
        =======    ======    =====    ========
        w1         w2        f        singular
        =======    ======    =====    ========
        bile       salts     30370    salt
        tree       leaves    30015    leaf
        maple      leafs     29701    leaf
        =======    ======    =====    ========  
        
    """
    w1 = models.CharField(max_length = 40)
    w2 = models.CharField(max_length = 40)
    singular = models.CharField(max_length = 40, blank = True)
    f = models.PositiveIntegerField(default = 0)
    objects = GetOrNoneManager()
    
    def __str__(self):
        return " ".join((self.w1, self.w2, str(self.f), self.singular))
    
    
    class Meta:
        unique_together = ('w1', 'w2', 'singular')
        ordering = ['-f']


class UnbracketedColorBigram(models.Model):
    """Unbracketed bigrams.
    
    **Fields:**
        | w1 (CharField): first word, ``max_length = 40``.
        | w2 (CharField): second word, ``max_length = 40``.
        | f (PositiveIntegerField): bigram's frequency  
        
    Sample entries:
    
        =======    =======    =
        w1         w2         f
        =======    =======    =
        summer     storm      2302
        lobster    bisque     2284
        tan        leather    2282
        =======    =======    =
    """
    w1 = models.CharField(max_length = 40)
    w2 = models.CharField(max_length = 40)
    f = models.PositiveIntegerField(default = 0)
    objects = GetOrNoneManager()
    
    def __str__(self):
        return " ".join((self.w1, self.w2, str(self.f)))
    
    class Meta:
        unique_together = ('w1', 'w2')
        ordering = ['-f']
        
        
class TweetImage(models.Model):
    '''Basic models for images used in tweets.'''
    created = models.DateTimeField(auto_now_add = True)
    # Original image 
    original = models.ImageField(upload_to = settings.ORIGINAL_IMAGE_UPLOAD_PATH, max_length = 1000)
    # Processed image (text added, filtered, etc.)
    processed = models.ImageField(upload_to = settings.PROCESSED_IMAGE_UPLOAD_PATH, max_length = 1000, blank = True)
    # Interjection used in processed image
    interjection = models.CharField(max_length = 50, blank = True)
    # Longer text used in processed image
    text = models.CharField(max_length = 1000, blank = True)

    objects = GetOrNoneManager()
    
    
class URLTweetImage(TweetImage):
    # URL to original image.
    url = models.URLField()
    
    objects = GetOrNoneManager()
    
    
class FlickrTweetImage(TweetImage):
    ''' Tweet image from Flickr.'''
    # Flickr ID of the image
    flickr_id = models.CharField(max_length = 200)
    # Flick user id
    flickr_user_id = models.CharField(max_length = 200)
    # Screen name of Flickr user.
    flickr_user_name = models.CharField(max_length = 200)
    # Flickr image secret
    flickr_secret = models.CharField(max_length = 200)
    # Flickr farm id
    flickr_farm = models.CharField(max_length = 200)
    # Flirck server id
    flickr_server = models.CharField(max_length = 200)
    # Title of the image
    title = models.CharField(max_length = 1000)
    # Longer description of the image
    description = models.TextField(max_length = 20000)
    
    objects = GetOrNoneManager()
    
    
    def get_flickr_url(self, size = 'z'):
        '''Get direct URL to image with specified size. See Flickr API 
        documentation for size strings.'''
        return "http://farm%s.static.flickr.com/%s/%s_%s_%s.jpg" % \
            (self.flickr_farm, self.flickr_server, self.flickr_id, self.flickr_secret, size)
            
    
        
        
class Tweet(models.Model):
    """Tweets made by the bot.
    
    **Fields:**
        | message (CharField): Tweet's text
        | muse (CharField): Class name of the used muse
        | context (CharField): Class name of the used context generator
        | color_code (CharField): Color code of the tweet, in html format.
        | color_name (CharField): Color name. 
        | value (Float): Appreciation of the tweet, estimates color_code - color_name - message mapping's aptness.
        | reasoning (TextField): Varying reasoning arguments.
        
    """
    tweeted = models.DateTimeField(auto_now_add = True)
    message = models.CharField(max_length = 160)
    muse = models.CharField(max_length = 100, default = "None")
    context = models.CharField(max_length = 100, default = "None")
    color_code = models.CharField(max_length = 10, default = "0xffffff")
    color_name = models.CharField(max_length = 100, default = "None")
    value = models.FloatField(default = 0.0)
    reasoning = models.TextField(default = "", null = True)
    objects = GetOrNoneManager()
    
    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ['-tweeted']
        

class ArticleTweet(Tweet):
    image = models.ForeignKey(FlickrTweetImage)
    article = models.URLField()
    objects = GetOrNoneManager()
     
        
class ReTweet(models.Model):
    """Tweets retweeted by the bot.
    
    **Fields:**
        | retweeted (DateTimeField): When the tweet was retweeted.
        | tweet_url (URlField): Original Tweet's Twitter URL
        | tweet_id (CharField): Original Tweet's Twitter id_str
        | screen_name (CharField): Screen name of the original tweeter.
        | tweet (ForeignKey): Reference to the bot's Tweet-model.
    """ 
    retweeted = models.DateTimeField(auto_now_add = True)
    tweet_url  = models.URLField(max_length = 200, null = True)
    screen_name = models.CharField(max_length = 200, null = True)
    tweet = models.ForeignKey(Tweet)
    objects = GetOrNoneManager()
        
    class Meta:
        ordering = ['-retweeted']  
        
