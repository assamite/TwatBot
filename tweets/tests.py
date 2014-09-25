"""
.. py:module:: tests
    :platform: Unix
    
Some tests for app's core functionalities, i.e. color manipulations.
"""
from django.utils import unittest
from django.test import TestCase

import color_utils as cu
from color_semantics import ColorSemantics

class ColorUtilsTestCase(TestCase):
    """Test case for color_utils-module."""
    
    def setUp(self):
        #TODO: randomize colors for some of the tests.
        self.html1 = "#ffffff"
        self.html2 = u'#000000'
        self.nhtml = "#ftgaas"
        self.hex1 = "0xffffff"
        self.hex2 = u'0x000000'
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
        self.assertEquals(cu.ed(self.html2, self.rgb2), 0.0, "color_utils.ed broken")
        self.assertEquals(cu.ed(self.html1, self.rgb2), 99.99998490087933, "color_utils.ed broken")
        
    
    def test_color_blending(self):
        """Test color blending."""
        self.assertEquals(cu.blend(self.html1, self.rgb2, a_head = 1.0), (255, 255, 255), "color_utils.blend broken")
        self.assertEquals(cu.blend(self.hex1, self.rgb2, a_head = 0.0), (0, 0, 0), "color_utils.blend broken")
        self.assertEquals(cu.blend(self.html1, self.hex2), (119, 119, 119), "color_utils.blend broken")
        self.assertEquals(cu.blend(self.rrgb, self.brgb), (202, 0, 137), "color_utils.blend broken")
    
        
class ColorSemanticsTestCase(TestCase):
    """Test case for color_semantics-module."""
    fixtures = ['test_fixtures.json']
    
    def setUp(self):
        self.semantics = ColorSemantics()
        self.green_codes = [u'#B0BF1A', u'#7FDD4C', u'#458B00', u'#C3C728', u'#64AC58', u'#8DB600', u'#69A577', u'#87A96B', u'#568203', u'#7EA660', u'#A1BEAE', u'#324F17', u'#839783', u'#8BA870', u'#6D7C4B', u'#93C460', u'#C0D9AF', u'#78866B', u'#7E8951', u'#ADFF2F', u'#2F847C', u'#9BD687', u'#7FFF00', u'#608341', u'#2A6241', u'#157D41', u'#9FA91F', u'#424D18', u'#B0D8CC', u'#2FBD78', u'#434F38', u'#4A5D23', u'#50C878', u'#6CB037', u'#4F7942', u'#228B22', u'#228B22', u'#228B22', u'#9AB78B', u'#006600', u'#D4D678', u'#A09238', u'#21422D', u'#58714A', u'#55C0A9', u'#243225', u'#29AB87', u'#9ACD32', u'#7CFC00', u'#008000', u'#76AA83', u'#C8E17B', u'#99A285', u'#BFFF00', u'#4FA93F', u'#73A55B', u'#3EB489', u'#4A5D23', u'#21421E', u'#6B8E23', u'#808000', u'#228B22', u'#6CA939', u'#7DB143', u'#E1E36E', u'#44743D', u'#01993D', u'#01796F', u'#CFB53B', u'#93C572', u'#87A96B', u'#9FC3A9', u'#4BA351', u'#507D2A', u'#228B22', u'#71EEB8', u'#5D7759', u'#009E60', u'#32CD32', u'#CFDBC5', u'#78AB46', u'#8BA870', u'#57A75B', u'#66BB66', u'#8EBD99', u'#008080', u'#8CBAA0', u'#228B22', u'#40E0D0', u'#43B3AE', u'#A2A415', u'#849137', u'#659D32', u'#CFCC8F', u'#A2C771', u'#516138']
        self.dists_html = [(0.0, u'#FFFFFF'), (0.34507772216326343, u'#FEFEFE'), (1.0360071048078772, u'#FCFCFC'), (1.2453575416990263, u'#FBFCFD')]
        self.dists_rgb = [(0.5798786270637373, (255, 8, 0)), (4.124449922053755, (255, 36, 0))]
        
        
    def test_semantic_basics(self):
        self.assertEquals(self.semantics.get_color_code('aubergine'), [u'#370028'])
        self.assertEquals(self.semantics.get_color_code('aubergine', frmt = 'rgb'), [(55, 0, 40)])
        self.assertEquals(self.semantics.get_color_code('green'), self.green_codes)
        self.assertEquals(self.semantics.get_color_code('isupposethisstringwillnotbetherebutthistestsucksstill'), None)
        
        self.assertEquals(self.semantics.get_color_string("#370028"), (u'aubergine', u'purple'))
        self.assertRaises(TypeError, self.semantics.get_color_string, "thisstringprobablyisnotcolorcodeeitherbutwillsucksstill")
        
        self.assertEquals(self.semantics.get_knn("#ffffff", k = 4), self.dists_html)
        self.assertEquals(self.semantics.get_knn("#ff0000", k = 2, frmt = 'rgb'), self.dists_rgb)