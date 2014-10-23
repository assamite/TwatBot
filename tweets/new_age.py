'''
.. py:module:: new_age
    :platform: Unix

New age personality affected by moon phases, etc.
'''
import ephem
import datetime
import bisect
import math

import numpy as np

from colormath.color_objects import sRGBColor, LabColor 

from tweets.utils import color as cu

# Precision used when describing the moon's phase in textual format,
# in phase_string().
PRECISION = 0.05
NEW =   0.0 / 4.0
FIRST = 1.0 / 4.0
FULL = 2.0 / 4.0
LAST = 3.0 / 4.0
NEXTNEW = 4.0 / 4.0

# MOON PHASE MAGICS: http://www.moonsmuses.com/moonphases.html
magics = {
    "new": ["love", "romance", "health", "hunting"],
    "waxing crescent": ["constructive", "love", "wealth", "success", "courage", "friendship", "luck", "health"],
    "first quarter": ["constructive", "love", "wealth", "success", "courage", "friendship", "luck", "health"],
    "waxing gibbous": ["constructive", "love", "wealth", "success", "courage", "friendship", "luck", "health"],
    "full": ["prophecy", "protection", "divination",  "love", "knowledge", "money", "dreams"],
    "waning gibbous": ["banish", "addiction", "detox", "illness", "negativity"],
    "last quarter": ["banish", "addiction", "detox", "illness", "negativity"],
    "waning crescent": ["detox", "anger", "passion", "understanding", "justice"]
    }

# AURA COLOR MEANINGS: http://www.reiki-for-holistic-health.com/auracolormeanings.html 
auras = {
    "#8B0000": {
        'name': 'deep red',
        'traits': ['grounded', 'realistic', 'active', 'strong willed', 'survival-oriented'],
        'relates': ['physical body', 'heart', 'circulation']
    }, 
    "#7F462C": {
        'name': 'muddied red',
        'traits': ['anger'],
        'relates': ['physical body', 'heart', 'circulation']
    },   
    "#EF1111": {
        'name': 'clear red',
        'traits': ['powerful', 'energetic', 'competitive', 'sexual', 'passionate'],
        'relates': ['physical body', 'heart', 'circulation']
    }, 
    "#FFC0CB": {
        'name': 'bright pink',
        'traits': ['loving', 'tender', 'sensitive', 'sensual', 'artistic', 'pure', 'compassionate'],
        'relates': ['clairaudience', 'romantic relationship']
    }, 
    "#FF4500": {
        'name': 'orange red',
        'traits': ['confident', 'creative'],
        'relates': []
    }, 
    "#FF9900": {
        'name': 'orange-yellow',
        'traits': ['creative', 'intelligent', 'detail oriented', 'perfectionist', 'scientific'],
        'relates': ['reproducive organs', 'emotions']
    },
    "#FFFFE0": {
        'name': 'pale yellow',
        'traits': ['awaking', 'inspiring', 'intelligent', 'creative', 'playful', 'optimistic', 'easy-going'],
        'relates': ['psychic awareness', 'spiritual awareness']
    }, 
    "#FFFACD": {
        'name': 'lemon',
        'traits': ['fearful', 'wary'],
        'relates': ['losing control']
    },
    "#FFD700": {
        'name': 'gold',
        'traits': ['inspiring'],
        'relates': ['spiritual energy', 'spiritual power']
    }, 
    "#BDB76B": {
        'name': 'dark yellow',
        'traits': ['over analytic', 'fatigued', 'stressed'],
        'relates': ['studying']
    },
    "#5B9C64": {
        'name': 'emerald green',
        'traits': ['love-centered', 'comforting', 'healing', 'social', 'teacher'],
        'relates': ['healing', 'growth', 'balance']
    }, 
    "#99CC32": {
        'name': 'yellow-green',
        'traits': ['communicative', 'creative'],
        'relates': []
    },
    "#006400": {
        'name': 'dark green',
        'traits': ['jealous', 'resentment', 'victimized', 'insecure'],
        'relates': ['lack of understanding', 'low self-esteem', 'sensitive to criticism']
    }, 
    "#40E0D0": {
        'name': 'turquoise',
        'traits': ['sensitive', 'compassionate', 'healing', 'therapist'],
        'relates': ['immune system']
    },
    "#D9E9FF": {
        'name': 'soft blue',
        'traits': ['caring', 'loving', 'peaceful', 'clear', 'bright', 'uncluttered', 'thruthful', 'intuitive'],
        'relates': ['caring', 'loving', 'sensitive', 'intuitive']
    }, 
    "#4169E1 ": {
        'name': 'royal blue',
        'traits': ['clairvoyant', 'generous'],
        'relates': ['high spiritual nature']
    },  
    "#00008B": {
        'name': 'dark blue',
        'traits': ['fearing'],
        'relates': ['fear of future', 'fear of self-expression', 'fear of speaking the truth']
    },
   "#12008B": {
        'name': 'indigo',
        'traits': ['intuitive', 'sensitive', 'deep feeling'],
        'relates': ['third eye', 'visual', 'pituitary gland']
    },
    "#8A2BE2": {
        'name': 'violet',
        'traits': ['intuitive', 'visionary', 'futuristic', 'idealistic', 'artistic', 'magical'],
        'relates': ['crown', 'pineal gland', 'nervous system']
    },
    "#E6E6FA": {
        'name': 'lavender',
        'traits': ['imaginative', 'visionary', 'daydreaming', 'etheric'],
        'relates': []
    },
    "#C0C0C0": {
        'name': 'silver',
        'traits': ['awaking', 'rich'],
        'relates': ['abundance']
    },
    "#BCC6CC": {
        'name': 'bright metallic silver',
        'traits': ['receptive', 'intuitive', 'nurturing'],
        'relates': []
    },
    "#666666": {
        'name': 'dark gray',
        'traits': ['unhealthy', 'stressed'],
        'relates': ['health problems']
    }, 
}

class NewAgePersonality():
    """New age personality traits for given date."""
    
    def __init__(self, date = datetime.date.today()):
        self.fate = date
        self.moon_phase = self.get_phase_on_day(date)
        self.moon_phase_string = self.get_phase_string(self.moon_phase)
    
    
    def get_phase_on_day(self, date = datetime.date.today()):
        """Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
        #Ephem stores its date numbers as floating points, which the following uses
        #to conveniently extract the percent time between one new moon and the next
        #This corresponds (somewhat roughly) to the phase of the moon.
        
        #Use Year, Month, Day as arguments
        date=ephem.Date(date)
        
        nnm = ephem.next_new_moon    (date)
        pnm = ephem.previous_new_moon(date)
        
        lunation=(date-pnm)/(nnm-pnm)
        
        #Note that there is a ephem.Moon().phase() command, but this returns the
        #percentage of the moon which is illuminated. This is not really what we want.
        
        return lunation
    
    def get_phase_string(self, lunation):
        p = lunation
        
        phase_strings = (
            (NEW + PRECISION, "new"),
            (FIRST - PRECISION, "waxing crescent"),
            (FIRST + PRECISION, "first quarter"),
            (FULL - PRECISION, "waxing gibbous"),
            (FULL + PRECISION, "full"),
            (LAST - PRECISION, "waning gibbous"),
            (LAST + PRECISION, "last quarter"),
            (NEXTNEW - PRECISION, "waning crescent"),
            (NEXTNEW + PRECISION, "new"))
    
        i = bisect.bisect([a[0] for a in phase_strings], p)
    
        return phase_strings[i][1]
    
    def get_mood(self, date = datetime.date.today()):
        lunation = self.get_phase_on_day(date)
        moon_phase = self.get_phase_string(lunation)
        aura_color = self.get_aura_color(lunation, date)
        
        return {'lunation': lunation, 'moon_phase': moon_phase, 'aura_color': aura_color}
        
        
    def get_aura_color(self, lunation, date = datetime.date.today()):   
        """Get aura color for given date with given lunation. 
        
        The lunation's correctness to the date is not checked.
        Lunation affects the *a*- and *b*-color opponent dimensions in LAB-color 
        space. Lightness depends on the time of the year. More precisely, how long
        the sun is above the horizon in Helsinki during the day, i.e. aura colors 
        tend to be darker during the winter.
        
        The exact formulas for *l*, *a* and *b* is::
            
            l = (sun_above_horizon / 24h)*100 + N(0, 40)
            a = sin(2 * PI * lunation)*80 + N(0, 30)
            b = cos(2 * PI * lunation)*80 + N(0, 30),
            
        where *N(0, X)* is normal distribution with zero mean and *X* variance.
        The lightness value is restricted to the interval [20, 100].     
        """  
        a, b = self.__lab_coordinate(lunation)
        na = a + np.random.normal(0, 30)
        nb = b + np.random.normal(0, 30)
        l = self.__get_lightness(date)  
        lc = LabColor(lab_l = l, lab_a = na, lab_b = nb)
        rgb = cu._lab2rgb(lc)
        return rgb
    
    
    def __get_lightness(self, date = datetime.date.today()):
        """"""
        hki = ephem.city('Helsinki')
        hki.date = date
        sun = ephem.Sun()
        nsr = ephem.localtime(hki.next_rising(sun))
        nss = ephem.localtime(hki.next_setting(sun))
        dt = nss - nsr
        seconds = float(dt.seconds)
        part_of_day = seconds / (24*60*60)
        lightness = (part_of_day * 100) + np.random.normal(0, 40)
        lightness = 20 if lightness < 20 else lightness
        lightness = 100 if lightness > 100 else lightness
        return lightness
    
    
    def __lab_coordinate(self, lunation):
        angle = 2 * math.pi * lunation
        a = math.sin(angle) * 80
        b = math.cos(angle) * 80
        return (a, b)
    
    
    
    
