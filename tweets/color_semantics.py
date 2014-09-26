"""
.. py:module:: color_semantics 
    :platform: Unix
    :synopsis: Semantic informed color manipulations.

Semantic informed color manipulations.

Color manipulations that are semantically informed, i.e. they have access to
database models for color information and linguistic readymades.
"""
import operator
import random

import tweets.color_utils as cu

from tweets.models import ColorMap, EveryColorBotTweet, UnbracketedColorBigram
from tweets.models import ColorUnigramSplit, ColorUnigram, PluralColorBigram
from tweets.models import Color

class ColorSemantics():
    """Master class for semantic informed color manipulations.
    
    Relevant color knowledge and linguistic readymade-information is loaded to 
    memory on initialization for faster data access.
   
    .. warning::
        You should not instantiate this class by yourself, instead use the automatically
        loaded class instance available at ``tweets.semantics``.
    """ 
    def __init__(self):
        self.reload_resources()
        
                   
    def reload_resources(self):
        """Reload resources from database into the object.
        
        .. note::
            Call this method only if you change database contents while the app is 
            running.
            
        """   
        self.colors_rgb = {}
        self.colors_html = {}
        cols = Color.objects.all()
        for c in cols:
            rgb = (c.rgb_r, c.rgb_g, c.rgb_b)
            self.colors_rgb[rgb] = (c.html, (c.l, c.a, c.b))
            self.colors_html[c.html] = (rgb, (c.l, c.a, c.b))
        
        self.color_map_html = {}
        self.color_map_ster = {}
        self.color_map_base = {}
        cm = ColorMap.objects.all()
        for c in cm:
            html = c.color.html
            self.color_map_html[html] = (c.stereotype, c.base_color)
            if c.stereotype in self.color_map_ster:
                self.color_map_ster[c.stereotype].append(html)
            else:
                self.color_map_ster[c.stereotype] = [html]
            if c.base_color in self.color_map_base:
                self.color_map_base[c.base_color].append(html)
            else:
                self.color_map_base[c.base_color] = [html]
            
        self.unigrams = {}
        ug = ColorUnigram.objects.all()
        for u in ug:
            self.unigrams[u.solid_compound] = u.f
            
        self.unigram_splits = []
        ugs = ColorUnigramSplit.objects.all()
        for u in ugs:
            self.unigram_splits.append((u.w1, u.w2))
         
        self.bigrams = {}
        bigs = UnbracketedColorBigram.objects.all()
        for b in bigs:
            self.bigrams[(b.w1, b.w2)] = b.f 
    

    def get_color_code(self, color_name, frmt = 'html'):
        """Find all color codes for color name from resources.
        
        Usually only one color code is returned if color name is a stereotype,
        and list if it is a base color name.
        
        **Args:**
            | color_name (str): Human readable color name. Either base color name or stereotype.
            | frmt (str): Format for returned colors, currently ``html`` and ``rgb`` are supported.          
            
        **Returns:**
            List of unicode strings. Color codes in specified format if color name was found from resources,
            None otherwise.
        """
        cl = []
        if color_name in self.color_map_ster:
            for html in self.color_map_ster[color_name]:
                cl.append(self.colors_html[html][0] if frmt == 'rgb' else html)
            return cl 
        elif color_name in self.color_map_base:
            for html in self.color_map_base[color_name]:
                cl.append(self.colors_html[html][0] if frmt == 'rgb' else html)
            return cl
        
        return None
    
    
    def get_color_string(self, color_code):
        """Get color stereotype and base name for color code from resources.
        
        **Args:**
            | color_code: Color code in any supported format. See supported formats from ``color_utils``-module.
            
        **Returns:**
            Tuple of unicode strings, (stereotype, base name) in human readable format if color 
            code was found from resources, None otherwise.
        """
        html = cu.rgb2html(cu._2rgb(color_code))
        if html in self.color_map_html: 
            return self.color_map_html[html]
        return None
    
     
    def get_knn(self, color_code, k = 1, frmt = 'html'):
        """Retrieve k-nearest color codes for given color code from resources.
        
        .. note:: 
            This function is not optimalized in anyway and thus may take quite
            some time while it parses through all the available colors.
            
        **Args:**
            | color_code:  Color code in any supported format. See supported formats from ``color_utils``-module.
            | k (int): Amount of nearest neighbors to return.
            | frmt (str): Format for returned colors, currently ``html`` and ``rgb`` are supported.
            
        **Returns:**
            List of tuples, (color code, distance) k-nearest colors from resources,
            where color code is an unicode string in specified format and distance
            is non-negative float.    
        """
        #TODO: remove asserts and replace with type error.
        assert(type(k) is int)
        assert(k > 0)
        color_dict = self.colors_html if frmt == 'html' else self.colors_rgb
        dists =  sorted(map(lambda c: (cu.ed(color_code, c), c), color_dict.keys()))
        return dists[:k]
    
    
    def blend_all_unigram_splits(self, frmt = 'html', **blend_options):
        """Convenience function to blend all loaded ``ColorUnigramSplit`` s. 
        
        In blending, ``w1`` is treated as head color and ``w2`` as modifier color.
        
        **Args:**
            | frmt (str): Format for returned colors, currently ``html`` and ``rgb`` are supported.
            | \**blend_options: Miscellaneous blend options as stated in ``color_utils.blend``.
        
        **Returns:**
            List of tuples (unigram split, blending), where unigram split is a
            (w1, w2)-tuple and ``blending`` is an tuple returned by ``ColorSemantics.blend``. 
        """
        ret = []
        for u in self.unigram_splits:
            try: 
                ret.append((u, self.blend(u[0], u[1], frmt = frmt, **blend_options))) 
            except LookupError: 
                # Do something with error
                print "Could not blend ", u[0], "and", u[1]
        return ret
    
    
    def blend(self, head, modifier, frmt = 'html', **blend_options):
        """Blend two colors identified by color names.
        
        Color names should be found resources, especially from color mappings.
        Names are first looked from color stereotypes and after that from base
        names. 
        
        .. note::
            Currently, if many matching color codes are found, the blended one
            is picked at random.
        
        **Args:**
            | head (str):  Name of the head color, either base name or color stereotype.
            | modifier (str):  Name of the modifier color, either base name or color stereotype.
            | frmt (str): Format for returned colors, currently ``html`` and ``rgb`` are supported.
            | \**blend_options: Miscellaneous blend options as stated in ``color_utils.blend``.
            
        **Returns:**
            Tuple of specified color formats, ``(chead, cmodifier, cblend)``, 
            where ``chead`` and the ``cmodifier`` are the used input colors and 
            ``cblend`` is the acquired color blending.
            
        """
        chead = self.get_color_code(head, frmt)
        cmodifier = self.get_color_code(modifier, frmt)
        if chead is None:
            raise LookupError("Could not find color matching the name %s from resources." % chead)
        if cmodifier is None:
            raise LookupError("Could not find color matching the name %s from resources." % chead)
        chead = random.choice(chead)
        cmodifier = random.choice(cmodifier)
        color_blend = cu.blend(chead, cmodifier, **blend_options)
        if frmt == 'html':
            color_blend = cu.rgb2html(color_blend)
        return (chead, cmodifier, color_blend)
        
        
    
        