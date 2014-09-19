"""
.. py:module: resources_utils
    :platform: Unix
    :synopsis: Utility functions to populate Django models with resources.
    
Utility functions to populate Django models with given resources. 

.. warning:: 
    As the functions don't restrict multiple instances of the same entry to be 
    added to the database, they should be used only once.
    
    It is suggested to run these once and then immediately use::
    
    $> python manage.py dumpdata --format=json --indent=4 > dbdump.json
    
    to save database contents to be able to load them as fixtures later, if the
    database models change.
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings

def populate_bracketed_color_bigrams(filepath):
    """Populate BracketedColorBigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *start_bracket, w1, w2, end_bracket, f*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from color_tweets.models import BracketedColorBigrams
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        sb, w1, w2, eb, f = e.split("\t")
        print "Reading: ", sb, w1, w2, eb, f
        instance = BracketedColorBigrams(start_bracket = sb, w1 = w1, w2 = w2,\
                                         end_bracket = eb, f = int(f))
        instance.save()


def populate_colormap(filepath):
    """Populate ColorMap model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *stereotype, color, html*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from color_tweets.models import ColorMap
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        s, c, html = e.split("\t")
        print "Reading: ", s, c, html
        instance = ColorMap(stereotype = s, color = c, html = html)
        instance.save()
        
        
def populate_color_unigrams(filepath):
    """Populate ColorUnigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *solid_compound, f*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from color_tweets.models import ColorUnigrams
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        s, f = e.split("\t")
        print "Reading: ", s, f
        instance = ColorUnigrams(solid_compound = s, f = int(f))
        instance.save()
        
        
def populate_everycolorbot_tweets(filepath):
    """Populate EveryColorBotTweets model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *hex, url*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from color_tweets.models import EveryColorBotTweets
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        h, u = e.split("\t")
        print "Reading: ", h, u
        instance = EveryColorBotTweets(hex = h, url = u)
        instance.save()
        
        
def populate_plural_color_bigrams(filepath):
    """Populate PluralColorBigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *w1, w2, f, singular*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from color_tweets.models import PluralColorBigrams
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        w1, w2, f, s = e.split("\t")
        print "Reading: ", w1, w2, f, s
        instance = PluralColorBigrams(w1 = w1, w2 = w2,\
                                         singular = s, f = int(f))
        instance.save()


def populate_unbracketed_color_bigrams(filepath):
    """Populate UnnracketedColorBigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *w1, w2, f*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from color_tweets.models import UnbracketedColorBigrams
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        w1, w2, f = e.split("\t")
        print "Reading: ", w1, w2, f
        instance = UnbracketedColorBigrams(w1 = w1, w2 = w2, f = int(f))
        instance.save()


def populate_default():
    """Call all distinct populate functions with default parameters.
    
    Default parameter for each model points into `../resources/<relevant_file_name>.tsv`.
    """
    populate_everycolorbot_tweets("../resources/everycolorbot_tweets.tsv")
    populate_plural_color_bigrams("../resources/plural_color_bigrams.tsv")
    populate_color_unigrams("../resources/color_unigrams.tsv")
    populate_colormap("../resources/color_map.tsv")
    populate_unbracketed_color_bigrams("../resources/unbracketed_color_bigrams.tsv")
    populate_bracketed_color_bigrams("../resources/bracketed_color_bigrams.tsv")
    