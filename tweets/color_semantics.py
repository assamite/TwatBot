"""
.. py:module:: semantics 
    :platform: Unix
    :synopsis: Semantic informed color manipulations.

Semantic informed color manipulations.

Color manipulations that are semantically informed, i.e. they have access to
database models for color information and linguistic readymades.
"""
from tweets.color_utils import *
from tweets.models import ColorMap, EveryColorBotTweet, UnbracketedColorBigram
from tweets.models import ColorUnigram, BracketedColorBigram, PluralColorBigram


def ColorSemantics():
    """Master class for semantic informed color manipulations. 
    
    You should not instance this class by yourself, instead use the automatically
    loaded class instance in package's semantics-attribute.
    """
    
    def __init__(self):
        print "Initialising ColorSemantics."
        cm = ColorMap.objects()
        for c in cm:
            print c
    

    def get_color_code(self, color_name):
        """Find color code for color name from resources.
        
        **Args:**
            | color_name (``str``): Human readable color name
            
        **Returns:**
            Color code in rgb-format if color name was found from resources,
            None otherwise.
        """
        
        pass
    
    
    def get_color_string(self, color_code):
        """Find color name for color code from resources.
        
        **Args:**
            | color_code: Color code in any supported format. See supported 
            formats from ``color_utils``-module.
            
        **Returns:**
            Human readable color name if color code was found from resources, 
            None otherwise.
        """
        
        pass
