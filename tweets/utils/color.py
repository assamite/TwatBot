"""

.. py:module:: color_utils
    :platform: Unix
    :synopsis: Different utility functions for working with colors.
    
Utility functions for working with colors.

Functions defined in this module are ignorant of semantics, and you should do your
reasoning, e.g. what to blend and how to blend, before calling functions in 
this module. 

The module relies on ``colormath``-package's functionality.
Furthermore, three light weight color definitions are supported for convenience:

* hex: ``str`` or ``unicode`` in form of ``0xrrggbb``, where ``r``, ``g`` and ``b`` are hex codes.
* html: ``str`` or ``unicode`` in form of ``#rrggbb``, where ``r``, ``g``, ``b`` are hex codes.
* rgb: ``tuple`` in form of ``(r, g, b)``, where ``r``, ``g`` and ``b`` are integers in [0, 255].

.. note::
    Some of the module's functions convert light weight color definitions into ``LabColor``-objects 
    (`colormath.color_objects <http://python-colormath.readthedocs.org/en/latest/color_objects.html>`_) 
    internally; especially blending and distance calculations are done in 
    `Lab color space <http://en.wikipedia.org/wiki/Lab_color_space>`_. Conversion between
    color spaces might (and will) cause some inaccuracies in colors due to needed floating 
    point operations.
"""
import re
from math import sqrt
from colormath.color_objects import sRGBColor, LabColor 
from colormath.color_conversions import convert_color
from PIL import Image
import tempfile

re_html = re.compile(r'^#[0-9a-fA-F]{6}$')
re_hex = re.compile(r'^0x[0-9a-fA-F]{6}$')

def is_rgb(rgb):
    """Verify that color variable is in accepted rgb-format.
    
    Accepted rgb-format is an integer 3-tuple with all values in [0, 255]
    
    **Args:**
        rgb (tuple): Variable to be verified.
        
    **Returns:**
        ``True`` if variable is in rgb-format, ``False`` otherwise.   
    """
    if type(rgb) is not tuple:
        return False
    if len(rgb) < 3:
        return False
    if not all(type(i) == int for i in rgb):
        return False
    if not all((i >= 0 and i <= 255) for i in rgb):
        return False
    return True


def is_html(html):
    """Verify that color variable is in accepted html-format.
    
    Accepted html-format is a string (or unicode string) in form of `#rrggbb``, where ``r``, ``g`` 
    and ``b`` are hex codes..
    
    **Args:**
        html: Variable to be verified.
        
    **Returns:**
        ``True`` if variable is in html-format, ``False`` otherwise.  
    """
    if type(html) is not str and type(html) is not unicode:
        return False
    if not re_html.match(html):
        return False
    return True


def is_hex(hex):
    """Verify that color variable is in accepted hex-format.
    
    Accepted hex-format is a string (or unicode string) in form of ``0xrrggbb``, where ``r``, ``g`` 
    and ``b`` are hex codes.
    
    **Args:**
        hex: Variable to be verified.
        
    **Returns:**
        ``True`` if variable is in hex-format, ``False`` otherwise.  
    """
    if type(hex) is not str and type(hex) is not unicode:
        return False
    if not re_hex.match(hex):
        return False
    return True


def _lab2rgb(c):
    """Convert LabColor into rgb-tuple.
    """
    if not type(c) is LabColor:
        raise TypeError("Variable not an instance of LabColor.")
    rgb = convert_color(c, sRGBColor).get_value_tuple()
    # Clamp out of gamut colors into [0, 1] since colormath package does not do it
    r, g, b = [(0.0 if a < 0.0 else 1.0 if a > 1.0 else a) for a in rgb]
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def _2lab(c):
    """Convert given color into colormath-packages LabColor object.
    
    *Args:**
        color: color in any supported format.
        
    **Returns:**
        LabColor object for given color.
    """
    r, g, b = _2rgb(c)
    return convert_color(sRGBColor(r, g, b, is_upscaled = True), LabColor)
    

def _2rgb(c):
    if not is_rgb(c):
        if is_html(c):
            return html2rgb(c)
        elif is_hex(c):
            return  hex2rgb(c)
        elif type(c) is LabColor:
            return _lab2rgb(c)    
        else:
            raise TypeError("Given variable is not in accepted format.")
    return c


def hex2rgb(hex):
    """Convert hex-string color into rgb-tuple.
    
    **Args:**
        hex (str): Color in hex-format, e.g. ``0xffeedd``.
    
    **Returns:**
        Color in rgb as 3-tuple, e.g. ``(255, 255, 255)``.
    """
    if not is_hex(hex):
        raise TypeError("Given variable is not in accepted hex-format.")
    return (int(hex[2:4], 16), int(hex[4:6], 16), int(hex[6:], 16))


def rgb2hex(rgb):
    """Convert rgb-tuple into hex-color string.
    
    **Args:**
        rgb (tuple): Color in rgb-format, e.g. ``(255, 255, 255)``.
    
    **Returns:**
        Color as hex-string, e.g. ``0xffeedd``.
    """
    if not is_rgb(rgb): 
        raise TypeError("Given variable is not in accepted rgb-format.")
    return "0x{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]) 


def html2rgb(html):
    """Convert html color format string into rgb-tuple.
    
    **Args:**
        html (str): color in html-format, e.g. ``#ffeedd``
    
    **Returns:**
        Color in rgb as 3-tuple, e.g. ``(255, 255, 255)``.
    """
    if not is_html(html):
        raise TypeError("Given variable is not in accepted html-format.")
    return (int(html[1:3], 16), int(html[3:5], 16), int(html[5:], 16))


def rgb2html(rgb):
    """Convert rgb-tuple into html color format string.
    
    **Args:**
        rgb (tuple): color in rgb-format, e.g. ``(255, 255, 255)``
    
    **Returns:**
        Color in html-format string, e.g. ``#ffeedd``.
    """
    if not is_rgb(rgb): 
        raise TypeError("Given variable is not in accepted rgb-format.")
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]) 
   
    
def blend(head, modifier, **kwargs):
    """Blend two colors in Lab color space.
    
    Blending of colors is done based on optional keyword arguments that are 
    given to the function. If no arguments are given, blending is a mean of 
    the Lab-values of input colors.
    
    .. note:: 
        Floating point operations might cause some inaccuracies in colors when
        changing to and from Lab color space.
    
    **Args:** 
        | head: head color in any supported format.    
        | modifier: modifier color in any supported format.
        | kwargs: Optional blending instructions. Currently supported keyword arguments are:
        
            | a_head (float): amount of head color to mix. Should be in [0, 1]. 
            | a_lab (tuple): amount of each head color component to 
            | mix, each value in tuple should be in [0, 1].
            
        | If a_lab is present, a_head is ignored. 
    
    **Returns:**
        Blended color as rgb-tuple.
    """
    h = _2lab(head).get_value_tuple()
    m = _2lab(modifier).get_value_tuple()  
    a_lab = (0.5, 0.5, 0.5)
    if kwargs:
        if 'a_lab' in kwargs:
            a_lab = kwargs['a_lab'] 
        elif 'a_head' in kwargs:
            a_head = kwargs['a_head']
            a_lab = (a_head, a_head, a_head)
            
    l = (a_lab[0] * h[0] + (1 - a_lab[0]) * m[0])
    a = (a_lab[1] * h[1] + (1 - a_lab[1]) * m[1])
    b = (a_lab[2] * h[2] + (1 - a_lab[2]) * m[2])
    return _2rgb(LabColor(l, a, b))


def ed(color1, color2):
    """Euclidean distance between two colors.
    
    The distance calculation is done in CIE Lab color space. 
    Input colors can be in any supported format.
    
    **Args:**
        | color1: first color
        | color2: second color
        
    **Returns:**
        Distance between colors as ``float``.
    """
    l1, a1, b1 = _2lab(color1).get_value_tuple()
    l2, a2, b2 = _2lab(color2).get_value_tuple()
    return sqrt((l1 - l2)**2 + (a1 - a2)**2 + (b1 - b2)**2)


def get_closest(color_code, color_list):
    """Get color closest to color code from the color list.
    
    **Returns:**
        Tuple, (distance, color code)
    """
    if type(color_list) is not list or len(color_list) == 0:
        raise ValueError("Color list should be non-empty list.")
    min_ed = ed(color_code, color_list[0])
    cur = color_list[0]
    for c in color_list[1:]:
        cur_ed = ed(color_code, c)
        if cur_ed < min_ed:
            min_ed = cur_ed
            cur = c
    return (min_ed, cur)
    
    
def create_temp_image(size, color_code):
    """Create temporal jpg-image of the color code.
    
    File is deleted when it is closed.
    
    **Args:**
        | size (tuple): (int, int), dimensions for the image
        | color_code: Color in any supported format.
        
    **Returns:**
        NamedTemporaryFile, file's name has '.jpg'-suffix.
    """
    im = Image.new('RGB', size, _2rgb(color_code))
    tmp = tempfile.NamedTemporaryFile(suffix = ".jpg")
    im.save(tmp, "JPEG")
    return tmp
    
            
    
    
