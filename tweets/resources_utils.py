"""
.. py:module:: resources_utils
    :platform: Unix
    :synopsis: Utility functions to populate Django models with resources.
    
Utility functions to populate Django models with given resources. 

.. warning:: 
    As these functions don't restrict multiple instances of the same entry to be 
    added to the database, they should be used only once.
    
    It is suggested to run these only once, and then immediately use::
    
    $> python manage.py dumpdata --format=json --indent=4 > color_tweets/fixtures/dbdump.json
    
    to save database contents so that the dump can be used as a fixture,
    if database needs to be repopulated.
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'
from django.conf import settings

def populate_bracketed_color_bigrams(filepath = "../resources/bracketed_color_bigrams.tsv"):
    """Populate BracketedColorBigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *start_bracket, w1, w2, end_bracket, f*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from tweets.models import BracketedColorBigram
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        sb, w1, w2, eb, f = e.split("\t")
        print "Reading: ", sb, w1, w2, eb, f
        instance = BracketedColorBigram(start_bracket = sb, w1 = w1, w2 = w2,\
                                         end_bracket = eb, f = int(f))
        instance.save()


def populate_colormap(filepath = "../resources/color_map.tsv"):
    """Populate ColorMap model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *stereotype, color, html*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from tweets.models import ColorMap, Color
    import tweets.color_utils as cu
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        s, c, html = e.split("\t")
        print "Reading: ", s, c, html
        html = html.strip()
        R, G, B = cu.html2rgb(html)
        chex = cu.rgb2hex((R, G, B))
        l, a, b = (cu.__2lab((R, G, B))).get_value_tuple()
        color_inst = Color.objects.get_or_none(html = html)                                                   
        if color_inst is None:
            color_inst = Color(html = html, hex = chex, rgb_r = R, rgb_g = G, rgb_b = B, l = l, a = a, b = b)
            color_inst.save()
        instance = ColorMap(stereotype = s, base_color = c, color = color_inst)
        instance.save()
        
        
def populate_color_unigrams(filepath = "../resources/color_unigrams.tsv"):
    """Populate ColorUnigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *solid_compound, f*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from tweets.models import ColorUnigram
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        s, f = e.split("\t")
        print "Reading: ", s, f
        instance = ColorUnigram(solid_compound = s, f = int(f))
        instance.save()
        
        
def populate_everycolorbot_tweets(filepath = "../resources/everycolorbot_tweets.tsv"):
    """Populate EveryColorBotTweets model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *hex, url*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from tweets.models import EveryColorBotTweet, Color
    import tweets.color_utils as cu
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        chex, u = e.split("\t")
        print "Reading: ", chex, u
        R, G, B = cu.hex2rgb(chex)
        html = cu.rgb2html((R, G, B))
        l, a, b = (cu.__2lab((R, G, B))).get_value_tuple()
        color_inst = Color.objects.get_or_none(html = html)                                                   
        if color_inst is None:
            color_inst = Color(html = html, hex = chex, rgb_r = R, rgb_g = G, rgb_b = B, l = l, a = a, b = b)
            color_inst.save()
        instance = EveryColorBotTweet(url = u, color = color_inst)
        instance.save()
        
        
def populate_plural_color_bigrams(filepath = "../resources/plural_color_bigrams.tsv"):
    """Populate PluralColorBigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *w1, w2, f, singular*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from tweets.models import PluralColorBigram
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        w1, w2, f, s = e.split("\t")
        print "Reading: ", w1, w2, f, s
        instance = PluralColorBigram(w1 = w1, w2 = w2,\
                                         singular = s, f = int(f))
        instance.save()


def populate_unbracketed_color_bigrams(filepath = "../resources/unbracketed_color_bigrams.tsv"):
    """Populate UnnracketedColorBigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *w1, w2, f*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    from tweets.models import UnbracketedColorBigram
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        w1, w2, f = e.split("\t")
        print "Reading: ", w1, w2, f
        instance = UnbracketedColorBigram(w1 = w1, w2 = w2, f = int(f))
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
    
    
if __name__ == "__main__":
    populate_default()   
    