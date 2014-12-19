''' 
.. py:module:: image
    :platform: Unix
    
Image processing functions and utilities. 

.. warning:: 

    The module needs `PIL <http://www.pythonware.com/products/pil/>`_ and 
    `G'MIC command line tool <http://gmic.eu/>`_ to work.
'''
import shlex
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageOps
import traceback
import subprocess
from tempfile import NamedTemporaryFile


def text2image(image, text, font_file = None, font_color = (128, 128, 128, 128),\
               background_color = None,\
               font_size = 12, scale_font = True, x_pos = 'center',\
               y_pos = 'center', max_x = 0.75, save_path = None):
    '''Add text with given color and background to image
    
    :param image: Image to alter
    :type image: PIL Image
    :param text: Text to add to the image
    :type text: str
    :param font_file: File for the truetype font to be used for the text
    :type font_file: str
    :param font_color: Font color as RGBA 
    :type font_color: tuple
    :param font_size: Font size in pixels
    :type font_size: int
    :param scale_font: Scale font size automatically to fit most of the image
    :type scale_font: int
    :param x_pos: X-axis position for the text. Supported: left, center, right, defaults to: center
    :type x_pos: str
    :param y_pos: Y-axis position for the text. Supported: top, center, down, defaults to:center
    :type y_pos: str
    :param save_path: Optional, path to save the image
    :type save_path: str
    :returns: Image - modified image

    '''
    if font_file is None:
        font_file = os.path.join(os.path.dirname(__file__), 'fonts', 'nevis.ttf')
        
    print font_file
    
    if scale_font:
        font_size = 8
    
    font = ImageFont.truetype(font_file, font_size)
    W, H = image.size
    text_mask = Image.new('RGBA', (W, H), (0,0,0,0))
    
    fw, fh = font.getsize(text) 
    if scale_font:
        font, fw, fh = _get_scaled_font(font_file, text, W, H, max_x)
     
    p = _get_text_pos((W,H), (fw, fh), x_pos, y_pos)
    
    draw_text = ImageDraw.Draw(text_mask)  
    if background_color is not None:
        draw_text.rectangle((p, (p[0] + fw, p[1] + fh)), background_color)
    draw_text.text(p, text, font = font, fill = font_color) 
    image = image.convert("RGBA")
    image.paste(text_mask, (0,0), text_mask)
    if save_path is not None:
        image.save(save_path)
        
    return image


def _get_scaled_font(font_file, text, W, H, max_x = 0.75, max_y = 0.75):
    font_size = 8
    font = ImageFont.truetype(font_file, font_size)
    fw, fh = font.getsize(text) 
    max_fw = W * max_x
    max_fh = H * max_y
    while (fw <= max_fw and fh <= max_fh):
        font_size += 2
        font = ImageFont.truetype(font_file, font_size)
        fw, fh = font.getsize(text)
    return font, fw, fh
    

def _get_text_pos(img_size, text_size, x_pos, y_pos):
    W, H = img_size
    w, h = text_size
    p = [20, 20]
    if x_pos == 'center': p[0] = (W - w) / 2
    if x_pos == 'left'  : p[0] = 20
    if x_pos == 'right' : p[0] = W - w - 20
    if y_pos == 'center': p[1] = (H - h) / 2
    if y_pos == 'top'   : p[1] = 20
    if y_pos == 'down'  : p[1] = H - h - 20
    return tuple(p)


def create_hope(image_path, word, save_path = None):
    '''Create poster in the colors of `HOPE-poster <http://en.wikipedia.org/wiki/Barack_Obama_%22Hope%22_poster>`_.
    
    The given word is added on the bottom of the image with dark blue background
    and light blue font color.
    
    :param image: Image to convert into a poster
    :type image: PIL Image
    :param word: Word to put in the place of "HOPE".
    :type word: str
    :returns: PIL Image -- created poster, or None if poster could not be created
    '''
    tmp = NamedTemporaryFile(suffix = '.png')
    cmd = "gmic {0} -blur 2,1 -poster_hope 3 -output {1}".format(image_path, tmp.name)
    cmd_args = shlex.split(cmd)
    try:
        p1 = subprocess.Popen(cmd_args)
        p1.wait()
    except:
        print traceback.format_exc()
        return None
    
    img = Image.open(tmp.name)
    W, H = img.size
    font, fw, fh = _get_scaled_font('./fonts/nevis.ttf', word, W, H, max_x = 0.9, max_y = 0.25)
    dark_blue = (0, 32, 47, 255)
    light_blue = (90, 141, 145, 255) 
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, H-fh),(W, H)), fill = dark_blue)
    draw.text(((W - fw) / 2, H-fh), word, font = font, fill = light_blue)
    
    if save_path is not None:
        img.save(save_path)
      
    return img

    
    
if __name__ == "__main__":
    
    img = Image.open("/Users/pihatonttu/Desktop/monkey.jpg")
    font_file = "./fonts/nevis.ttf"
    image = text2image(img, 'Original image by Plaaplaa @ Flickr', font_file = font_file, background_color = (255, 255, 255, 100), font_color = (0, 0, 0, 255), font_size = 10, y_pos = 'down', x_pos = 'right', scale_font = False)
    image = text2image(image, "SHEEESH!", font_file = font_file, font_color = (255, 255, 60, 128))
    image.show()
    '''
    image = create_hope("/Users/pihatonttu/git/TwatBot/tweets/utils/monkey.jpg", 'HUH')
    image.show()
    '''
    

