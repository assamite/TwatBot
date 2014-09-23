"""
.. py:module:: color_semantics 
    :platform: Unix
    :synopsis: Semantic informed color manipulations.

Semantic informed color manipulations.

Color manipulations that are semantically informed, i.e. they have access to
database models for color information and linguistic readymades.
"""
import tweets.color_utils as cu
from tweets.models import ColorMap, EveryColorBotTweet, UnbracketedColorBigram
from tweets.models import ColorUnigram, PluralColorBigram
from tweets.models import Color


class ColorSemantics():
    """Master class for semantic informed color manipulations.
    
    All color knowledge and linguistic readymade-information is loaded to memory
    on initialisation for faster data access.
   
    .. warning::
        You should not instance this class by yourself, instead use the automatically
        loaded class instance in package's semantics-attribute.
    """
    
    def __init__(self):
        self.colors = {}
        cols = Color.objects.all()
        for c in cols:
            rgb = (c.rgb_r, c.rgb_g, c.rgb_b)
            self.colors[rgb] = (c.html, (c.l, c.a, c.b))
            self.colors[c.html] = (rgb, (c.l, c.a, c.b))
        
        self.color_map = {}
        cm = ColorMap.objects.all()
        for c in cm:
            html = c.color.html
            self.color_map[html] = (c.stereotype, c.base_color)
            if c.stereotype in self.color_map:
                self.color_map[c.stereotype].append(html)
            else:
                self.color_map[c.stereotype] = [html]
            if c.base_color in self.color_map:
                self.color_map[c.base_color].append(html)
            else:
                self.color_map[c.base_color] = [html]
            
        self.unigrams = {}
        ugs = ColorUnigram.objects.all()
        for u in ugs:
            self.unigrams[u.solid_compound] = u.f
            
        self.bigrams = {}
        bigs = UnbracketedColorBigram.objects.all()
        for b in bigs:
            self.bigrams[(b.w1, b.w2)] = b.f
            
    

    def get_color_code(self, color_name):
        """Find all color codes for color name from resources.
        
        **Args:**
            | color_name (``str``): Human readable color name. Either base color name or stereotype.
            
        **Returns:**
            List of color codes in rgb-format if color name was found from resources,
            None otherwise.
        """
        cl = []
        if color_name in self.color_map:
            for html in self.color_map[color_name]:
                cl.append(self.colors[html][0])
            return cl 
        return None
    
    
    def get_color_string(self, color_code):
        """Find color stereotype and base name for color code from resources.
        
        **Args:**
            | color_code: Color code in any supported format. See supported 
            | formats from ``color_utils``-module.
            
        **Returns:**
            Tuple, (stereotype, base name) as human readable strings if color 
            code was found from resources, None otherwise.
        """
        html = cu.rgb2html(cu._2rgb(color_code))
        if html in self.color_map: 
            return self.color_map[html]
        return None
