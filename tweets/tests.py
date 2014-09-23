"""
.. py:module:: tests
    :platform: Unix
    
Some tests for app's core functionalities, i.e. color manipulations.
"""
from django.utils import unittest
from django.test import TestCase

import color_utils as cu

class ColorUtilsTestCase(TestCase):
    """Test case for color_utils-module."""
    
    def setUp(self):
        #TODO: randomize colors for some of the tests.
        self.html1 = "#ffffff"
        self.html2 = "#000000"
        self.nhtml = "#ftgaas"
        self.hex1 = "0xffffff"
        self.hex2 = "0x000000"
        self.nhex = "0xftgaas"
        self.rgb1 = (255, 255, 255)
        self.rgb2 = (0, 0, 0)
        self.brgb = (0, 0, 255)
        self.rrgb = (255, 0, 0);
        self.lab1 = (1.0, 1.0, 1.0)
        self.lab2 = (0.0, 0.0, 0.0)
    
    
    def test_color_validations(self):
        """Test color validations."""
        self.assertTrue(cu.is_rgb(self.rgb1), "color_utils.is_rgb broken.")
        self.assertTrue(cu.is_rgb(self.rgb2), "color_utils.is_rgb broken.")
        self.assertFalse(cu.is_rgb(self.html1), "color_utils.is_rgb broken.")
        self.assertFalse(cu.is_rgb((0, 0)), "color_utils.is_rgb broken.")
        
        self.assertTrue(cu.is_html(self.html1), "color_utils.is_html broken.")
        self.assertTrue(cu.is_html(self.html2), "color_utils.is_html broken.")
        self.assertFalse(cu.is_html(self.nhtml), "color_utils.is_html broken.")
        self.assertFalse(cu.is_html(self.rgb1), "color_utils.is_html broken.")
        self.assertFalse(cu.is_html(self.hex1), "color_utils.is_html broken.")
        
        self.assertTrue(cu.is_hex(self.hex1), "color_utils.is_hex broken.")
        self.assertTrue(cu.is_hex(self.hex2), "color_utils.is_hex broken.")
        self.assertFalse(cu.is_hex(self.nhex), "color_utils.is_hex broken.")
        self.assertFalse(cu.is_hex(self.rgb1), "color_utils.is_hex broken.")
        self.assertFalse(cu.is_hex(self.html1), "color_utils.is_hex broken.")
        
        
    def test_color_conversions(self):
        """Test different color conversion."""
        self.assertTrue(cu.is_rgb(cu.html2rgb(self.html1)), "color_utils.html2rgb broken.")
        self.assertTrue(cu.is_rgb(cu.hex2rgb(self.hex1)), "color_utils.hex2rgb broken.")
        self.assertTrue(cu.is_html(cu.rgb2html(self.rgb1)), "color_utils.rgb2html broken.")
        self.assertTrue(cu.is_hex(cu.rgb2hex(self.rgb2)), "color_utils.rgb2hex broken.")
        self.assertTrue(cu.is_rgb(cu._2rgb(self.html2)), "color_utils._2rgb broken.")
        self.assertTrue(cu.is_rgb(cu._2rgb(self.hex2)), "color_utils._2rgb broken.")
        self.assertTrue(cu.is_rgb(cu._2rgb(self.rgb1)), "color_utils._2rgb broken.")
        self.assertEquals(cu._2rgb(self.rgb1), self.rgb1, "color_utils._2rgb broken." )
       
        
    def test_color_distance(self):
        """Test color distance calculation."""
        self.assertEquals(cu.ed(self.html1, self.hex1), 0.0, "color_utils.ed broken")
        self.assertEquals(cu.ed(self.html1, self.rgb1), 0.0, "color_utils.ed broken")
        self.assertEquals(cu.ed(self.html1, self.rgb2), 99.99998489982414, "color_utils.ed broken")
        
    
    def test_color_blending(self):
        """Test color blending."""
        self.assertEquals(cu.blend(self.html1, self.rgb2, a_head = 1.0), (255, 255, 255), "color_utils.blend broken")
        self.assertEquals(cu.blend(self.hex1, self.rgb2, a_head = 0.0), (0, 0, 0), "color_utils.blend broken")
        self.assertEquals(cu.blend(self.html1, self.hex2), (119, 119, 119), "color_utils.blend broken")
        self.assertEquals(cu.blend(self.rrgb, self.brgb), (202, 0, 137), "color_utils.blend broken")
    
        
