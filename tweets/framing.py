"""

.. py:module:: framing
    :platform: Unix
    :synopsis: Tweet framing.
    
Module for framing the color code tweets.    
"""
from contexts import TextContext

def frame(context ='text', **kwargs):
    """Frame the tweet with given context and context related keyword arguments.
    
    .. warning:: 
        Currently half dummy implementation which uses TextContext always.
    
    First creates color name for color code and then frames the tweet for the
    color in given context.
    
    **Args:**
        | context (str): Context to frame tweet into. Should be one of the supported formats. 
        | \**kwargs: Keyword arguments for the given context. Should at least contain ``color_code`` -key.
    
    **Returns:**
        Tuple, ``(tweet, value)``, where ``tweet`` is the tweet for the color code
        in given context and ``value`` is a float estimating the color code-
        color name-framing mapping's interestingness and appreciation.
    
    """
    # Decide for the color name based on the color semantics
    from tweets.core import COLOR_SEMANTICS as semantics
    color_code = kwargs['color_code']
    color_name = semantics.name_color(color_code)
    
    if context == 'text':
        context = TextContext()
    else:
        context = TextContext()
    msg = context.build_tweet(color_name, **kwargs)
    
    return (msg, 0.0)
