"""
.. py:module:: resources_utils
    :platform: Unix
    :synopsis: Utility functions to populate Django models with resources.
    
Utility functions to populate Django models with given resources. 

.. warning:: 
    As these functions don't restrict multiple instances of the same entry to be 
    added to the database, they should be used with caution. The basic resources
    from ``project_root/resources/`` have already been converted into 
    json-fixture, which is available in ``project_root/tweets/fixtures/fixtures.json``.
    
    It is advised to use the fixture in order to repopulate the database after 
    migrations and to use functions defined here only to add new content afterwards.
    
    After adding the content, new database fixture can then be created as::
    
    $> cd project_root/
    $> python manage.py dumpdata --format=json --indent=4 tweets > tweets/fixtures/fixtures.json
    
    For more info about working with Django and initial model data, see 
    `Django's documentation <https://docs.djangoproject.com/en/1.6/howto/initial-data/>`_. 
    
"""
import os
import sys

def __set_django():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwatBot.settings'

def populate_bracketed_color_bigrams(filepath = "../resources/bracketed_color_bigrams.tsv"):
    """Populate BracketedColorBigrams model with entries found from file.
    
    File should be in tab separated format, where each line has model fields
    in the following order: *start_bracket, w1, w2, end_bracket, f*. 
    
    .. note::
        The first line of the file is though to contain field names and is omitted.
    
    **Args**
        | filepath (``str``): Path to the file with entries.
    """
    __set_django()
    from tweets.models import BracketedColorBigram
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        sb, w1, w2, eb, f = e.strip().split("\t")
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
    __set_django()
    from tweets.models import ColorMap, Color
    import tweets.color_utils as cu
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        s, c, html = e.strip().split("\t")
        print "Reading: ", s, c, html
        html = html.strip()
        R, G, B = cu.html2rgb(html)
        chex = cu.rgb2hex((R, G, B))
        l, a, b = (cu._2lab((R, G, B))).get_value_tuple()
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
    __set_django()
    from tweets.models import ColorUnigram
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        s, f = e.strip().split("\t")
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
    __set_django()
    from tweets.models import EveryColorBotTweet, Color
    import tweets.color_utils as cu
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        chex, u = e.strip().split("\t")
        print "Reading: ", chex, u
        R, G, B = cu.hex2rgb(chex)
        html = cu.rgb2html((R, G, B))
        l, a, b = (cu._2lab((R, G, B))).get_value_tuple()
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
    __set_django()
    from tweets.models import PluralColorBigram
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        w1, w2, f, s = e.strip().split("\t")
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
    __set_django()
    from tweets.models import UnbracketedColorBigram
    
    with open(filepath, 'r') as filehandle:
        entries = filehandle.readlines()
        
    for e in entries[1:]:
        w1, w2, f = e.strip().split("\t")
        print "Reading: ", w1, w2, f
        instance = UnbracketedColorBigram(w1 = w1, w2 = w2, f = int(f))
        instance.save()


def split_unigrams():
    """Split ColorUnigram-instances from database into two words and save them into
    ColorUnigramSplit-model.
    """
    __set_django()
    from tweets.models import ColorUnigram, ColorUnigramSplit, ColorMap
    colormaps = ColorMap.objects.all()
    colornames = set()
    for c in colormaps:
        colornames.add(c.stereotype)
        colornames.add(c.base_color)
        
    colornames = sorted(colornames)
    unigrams = ColorUnigram.objects.all()
    splits = []
    for u in unigrams:
        solid = u.solid_compound
        for c in colornames:
            if solid.startswith(c):
                if solid[len(c):] in colornames:
                    w1 = solid[:len(c)]
                    w2 = solid[len(c):] 
                    print w1, w2
                    splits.append((w1, w2))
                    if ColorUnigramSplit.objects.get_or_none(w1 = w1, w2 = w2) is None:
                        cus = ColorUnigramSplit(w1 = w1, w2 = w2, original = u)
                        cus.save()
                    break    
    
    print "Found", len(splits), "splits from original", len(unigrams), "unigrams."


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
    split_unigrams()
    
    
if __name__ == "__main__":
    populate_default() 
    