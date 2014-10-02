'''
.. py:module:: contexts
    :platform: Unix
    
Contexts for framing the tweets. 
'''
from abc import ABCMeta

class Context():
    """Abstract base class for contexts.
    
    .. note::
        Create a child class of this and override ``build_tweet`` -method.
    """
    
    class Meta:
        __metaclass__ = ABCMeta
     
    def build_tweet(self, color_code, color_name, **kwargs):
        """Build tweet for color and its name.
        
        .. note:: 
            Override in child class!
        """
        return "%s %s" % (color_code, color_name)
    
    
class TextContext(Context):
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
            return "@everycolorbot Gee, that's a nice color. I call it %s." % color_name
        return "By hard thinking, I have come to the conclusion that color %s is called %s. #geniusatwork" % (color_code, color_name)
