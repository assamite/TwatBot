"""
.. py:module:: models
    :platform: Unix
    :synopsis: Django models for resources given on the course.

Django models for resources given on the course.
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
        
    Sample entries:
        
        =============    =======    ======    ===========    =
        start_bracket    w1         w2        end_bracket    f
        =============    =======    ======    ===========    =
        and              cheddar    cheese        ,          3477
        the              eye        candy         .          3476
        with             wood       wool         and         3448
        =============    =======    ======    ===========    =    
     
    """   
    start_bracket = models.CharField(max_length = 40, blank = True)
    w1 = models.CharField(max_length = 40, blank = True)
    w2 = models.CharField(max_length = 40, blank = True)
    end_bracket = models.CharField(max_length = 40, blank = True)
    f = models.PositiveIntegerField(blank = True)


class ColorMap(models.Model):
    """Color stereotype - rgb (in html format) value pairs with base color names.
    
    **Fields:**
        | stereotype (``CharField``): Name of the color stereotype, ``max_length = 40``.
        | color (``CharField``): Base color, ``max_length = 40``.
        | html (``CharField``): Color in html-format, i.e. ``#rrggbb``, where ``r``, ``g`` and ``b`` are hex codes.   
        
    Sample entries:
    
        ==========    ======    ===
        stereotype    color     html
        ==========    ======    ===
        acid          green     #B0BF1A
        absinthe      green     #7FDD4C
        acorn         brown     #7F6241
        ==========    ======    ===    
         
    """ 
    stereotype = models.CharField(max_length = 40, blank = True)
    color = models.CharField(max_length = 40, blank = True)
    html = models.CharField(max_length = 7, blank = True)


class ColorUnigrams(models.Model):
    """Color unigrams.
    
    **Fields:**
        | solid_compound (``CharField``): Solid compound of the unigram, ``max_length = 50``.
        | f (``PositiveIntegerField``): unigram's frequency
        
    Sample entries: 
    
        ===============    =
        solid_compound     f
        ===============    =
        aluminumleather    594
        amberbunny         240
        amberdawn          300
        ===============    =    
    """   
    solid_compound = models.CharField(max_length = 50, blank = True)
    f = models.PositiveIntegerField(blank = True) 


class EveryColorBotTweets(models.Model):
    """ URL's and hex color codes for Everycolorbot's tweets.
    
    **Fields:**
        | hex (``CharField``): Color in hex-format, i.e. ``0xrrggbb``, where ``r``, ``g`` and ``b`` are hex codes. 
        | url (``URLField``): URL for the tweet.
         
    Sample entries:    
     
        ========    ====
        hex         url
        ========    ====
        0x634ef9    http://t.co/9OXdTPFOXK
        0x31a77c    http://t.co/99kdUpov9E
        0x98d3be    http://t.co/Os53Hh3qs7
        ========    ====

    """ 
    url = models.URLField(blank = True)
    hex = models.CharField(max_length = 8, blank = True)


class PluralColorBigrams(models.Model):
    """Plural color bigrams.
    
    **Fields:**
        | w1 (``CharField``): first word, ``max_length = 40``.
        | w2 (``CharField``): second word, ``max_length = 40``.
        | singular (``CharField``): singular of the second word, ``max_length = 40``.
        | f (``PositiveIntegerField``): bigram's frequency 
        
    Sample entries:
    
        =======    ======    =====    ========
        w1         w2        f        singular
        =======    ======    =====    ========
        bile       salts     30370    salt
        tree       leaves    30015    leaf
        maple      leafs     29701    leaf
        =======    ======    =====    ========  
        
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
        
    Sample entries:
    
        =======    =======    =
        w1         w2         f
        =======    =======    =
        summer     storm      2302
        lobster    bisque     2284
        tan        leather    2282
        =======    =======    =
    """
    w1 = models.CharField(max_length = 40, blank = True)
    w2 = models.CharField(max_length = 40, blank = True)
    f = models.PositiveIntegerField(blank = True)
