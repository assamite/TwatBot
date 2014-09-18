"""Django models for resources given on the course.
"""

from django.db import models


class BracketedColorBigrams(models.Model):
    """Bracketed bigrams.
    
    **Fields:**
        | start_bracket (``CharField``): starting bracket, ``max_length = 40``.
        | w1 (``CharField``): first word, ``max_length = 40``.
        | w2 (``CharField``): second word, ``max_length = 40``.
        | end_bracket (``CharField``): ending bracket, ``max_length = 40``.
        | f (``PositiveIntegerField``): bigram's frequency
    """   
    start_bracket = models.CharField(max_length = 40, blank = True)
    w1 = models.CharField(max_length = 40, blank = True)
    w2 = models.CharField(max_length = 40, blank = True)
    end_bracket = models.CharField(max_length = 40, blank = True)
    f = models.PositiveIntegerField(blank = True)


class ColorMap(models.Model):
    """Color stereotype - rgb (in html format) value pairs with base color names.
    
    Sample entries:
    
    ==========    ======    ===
    Stereotype    Color     Html
    ==========    ======    ===
    acid          green     #B0BF1A
    absinthe      green     #7FDD4C
    acorn         brown     #7F6241
    ==========    ======    ===
    
    **Fields:**
        | stereotype (``CharField``): Name of the color stereotype, ``max_length = 40``.
        | color (``CharField``): Base color, ``max_length = 40``.
        | html (``CharField``): Color in html-format, i.e. ``#rrggbb``, where ``r``, ``g`` and ``b`` are hex codes.    
    """ 
    stereotype = models.CharField(max_length = 40, blank = True)
    color = models.CharField(max_length = 40, blank = True)
    html = models.CharField(max_length = 7, blank = True)

class ColorUnigrams(models.Model):
    """Color unigrams.
    
    **Fields:**
        | solid_compound (``CharField``): Solid compound of the unigram, ``max_length = 50``.
        | f (``PositiveIntegerField``): unigram's frequency
    """   
    solid_compound = models.CharField(max_length = 50, blank = True)
    f = models.PositiveIntegerField(blank = True) 


class EveryColorBotTweets(models.Model):
    """ URL's and html color codes for Everycolorbot's tweets.
    
    **Fields:**
        | url (``URLField``): URL for the tweet.
        | html (``CharField``): Color in html-format, i.e. ``#rrggbb``, where ``r``, ``g`` and ``b`` are hex codes. 
    """ 
    url = models.URLField(blank = True)
    html = models.CharField(max_length = 7, blank = True)


class PluralColorBigrams(models.Model):
    """Plural color bigrams.
    
    **Fields:**
        | w1 (``CharField``): first word, ``max_length = 40``.
        | w2 (``CharField``): second word, ``max_length = 40``.
        | singular (``CharField``): singular of the second word, ``max_length = 40``.
        | f (``PositiveIntegerField``): bigram's frequency 
    """
    w1 = models.CharField(max_length = 40, blank = True)
    w2 = models.CharField(max_length = 40, blank = True)
    singular = models.CharField(max_length = 40, blank = True)
    f = models.PositiveIntegerField(blank = True)



class UnbracketedColorBigrams(models.Model):
    """Unbracketed bigrams.
    
    **Fields:**
        | w1 (``CharField``): first word, ``max_length = 40``.
        | w2 (``CharField``): second word, ``max_length = 40``.
        | f (``PositiveIntegerField``): bigram's frequency  
    """ 
    w1 = models.CharField(max_length = 40, blank = True)
    w2 = models.CharField(max_length = 40, blank = True)
    f = models.PositiveIntegerField(blank = True)
