"""

.. py:module:: color_utils
    :platform: Unix
    :synopsis: Different utility functions for working with colors.
    
Utility functions for working with colors.

Supports three types of color definitions:

* hex:    ``str`` in form of ``0xrrggbb``, where ``r``, ``g`` and ``b`` are hex codes.
* html:    ``str`` in form of ``#rrggbb``, where ``r``, ``g``, ``b`` are hex codes.
* rgb:    ``tuple`` in form of ``(r, g, b)``, where ``r``, ``g`` and ``b`` are integers in [0, 255].

.. note:: 
    Functions defined in this module are ignorant of semantics, and you should do your
    reasoning, e.g. what to blend and how to blend, before calling functions in 
    this module.
"""
import re
from math import sqrt

re_html = re.compile(r'^#[0-9a-fA-F]{6}$')
re_hex = re.compile(r'^0x[0-9a-fA-F]{6}$')

def is_rgb(rgb):
    """Verify that color variable is in accepted rgb-format.
    
    Accepted rgb-format is an integer 3-tuple with all values in [0, 255]
    
    **Args:**
        rgb (``tuple``): Variable to be verified.
        
    **Returns:**
        ``True`` if variable is in rgb-format, ``False`` otherwise.   
    """
    if type(rgb) is not tuple:
        return False
    if len(rgb) < 3:
        return False
    if not all((int(i) >= 0 and int(i) <= 255) for i in rgb):
        return False
    return True


def is_html(html):
    """Verify that color variable is in accepted html-format.
    
    Accepted html-format is a string in form of `#rrggbb``, where ``r``, ``g`` 
    and ``b`` are hex codes..
    
    **Args:**
        html (``str``): Variable to be verified.
        
    **Returns:**
        ``True`` if variable is in html-format, ``False`` otherwise.  
    """
    if type(html) is not str:
        return False
    if not re_html.match(html):
        return False
    return True


def is_hex(hex):
    """Verify that color variable is in accepted hex-format.
    
    Accepted hex-format is a string in form of ``0xrrggbb``, where ``r``, ``g`` 
    and ``b`` are hex codes.
    
    **Args:**
        hex (``str``): Variable to be verified.
        
    **Returns:**
        ``True`` if variable is in hex-format, ``False`` otherwise.  
    """
    if type(hex) is not str:
        return False
    if not re_hex.match(hex):
        return False
    return True


def __2rgb(c):
    if not is_rgb(c):
        if is_html(c):
            return html2rgb(c)
        elif is_hex(c):
            return  hex2rgb(c)
        else:
            raise TypeError("Given variable is not in accepted format.")
    return c


def hex2rgb(hex):
    """Convert hex-string color into rgb-tuple.
    
    **Args:**
        hex (``str``): Color in hex-format, e.g. ``0xffeedd``.
    
    **Returns:**
        Color in rgb as 3-tuple, e.g. ``(255, 255, 255)``.
    """
    if not is_hex(hex):
        raise TypeError("Given variable is not in accepted hex-format.")
    return (int(hex[2:4], 16), int(hex[4:6], 16), int(hex[6:], 16))


def rgb2hex(rgb):
    """Convert rgb-tuple into hex-color string.
    
    **Args:**
        rgb (``tuple``): Color in rgb-format, e.g. ``(255, 255, 255)``.
    
    **Returns:**
        Color as hex-string, e.g. ``0xffeedd``.
    """
    if not is_rgb(rgb): 
        raise TypeError("Given variable is not in accepted rgb-format.")
    return "0x{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]) 


def html2rgb(html):
    """Convert html color format string into rgb-tuple.
    
    **Args:**
        html (``str``): color in html-format, e.g. ``#ffeedd``
    
    **Returns:**
        Color in rgb as 3-tuple, e.g. ``(255, 255, 255)``.
    """
    if not is_html(html):
        raise TypeError("Given variable is not in accepted html-format.")
    return (int(html[1:3], 16), int(html[3:5], 16), int(html[5:], 16))


def rgb2html(rgb):
    """Convert rgb-tuple into html color format string.
    
    **Args:**
        rgb (``tuple``): color in rgb-format, e.g. ``(255, 255, 255)``
    
    **Returns:**
        Color in html-format string, e.g. ``#ffeedd``.
    """
    if not is_rgb(rgb): 
        raise TypeError("Given variable is not in accepted rgb-format.")
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]) 
    
    
def blend(head, modifier, **kwargs):
    """Blend two colors.
    
    Blending of colors is done based on optional keyword arguments that are 
    given to the function. If no arguments are given, blending is a mean of 
    the rgb-values of input colors.
    
    **Args:** 
        | head: head color in any supported format.    
        | modifier: modifier color in any supported format.
        | kwargs: Optional blending instructions. Currently supported keyword arguments are:
        
            | a_head (``float``): amount of head color to mix. Should be in [0, 1]. 
            | a_rgb (``tuple``): amount of each head color component to 
            | mix, each value in tuple should be in [0, 1].
            
        | If a_rgb is present, a_head is ignored. 
    
    **Returns:**
        Blended color as rgb-tuple.
    """
    h = __2rgb(head)
    m = __2rgb(modifier)  
    a_rgb = (0.5, 0.5, 0.5)
    if kwargs:
        if 'a_rgb' in kwargs:
            a_rgb = kwargs['a_rgb'] 
        elif 'a_head' in kwargs:
            a_head = kwargs['a_head']
            a_rgb = (a_head, a_head, a_head)
            
    r = int(a_rgb[0] * h[0] + (1 - a_rgb[0]) * m[0])
    g = int(a_rgb[1] * h[1] + (1 - a_rgb[1]) * m[1])
    b = int(a_rgb[2] * h[2] + (1 - a_rgb[2]) * m[2])  
    return (r, g, b)


def dist(color1, color2):
    """Calculate distance between two colors.
    
    Currently the distance is calculated between euclidean distance between
    rgb-tuples. Input colors can be in any supported format.
    
    **Args:**
        | color1: first color
        | color2: second color
        
    **Returns:**
        Distance between colors as ``float``.
    """
    c1 = __2rgb(color1)
    c2 = __2rgb(color2)
    return sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)
            
    
    
