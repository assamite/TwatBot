'''
.. py:module:: new_age
    :platform: Unix

New age personality affected by moon phases, etc.
'''
import sys
import ephem
import datetime
import bisect
import math
import random

import numpy as np

from colormath.color_objects import sRGBColor, LabColor 

from tweets.utils import color as cu
from tweets.utils.text import bag_of_words, sentiment
from web import therex, uclass
import loevheim_cube

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
    "#4169E1": {
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

# http://www.bestmoodrings.com/blog/mood-ring-color-chart-meanings
mood_colors = {              
    '#000000': {
        'name': 'black',
        'stereotype': ('fear', (20, 80)), # mood stereotype, happy-upset ratio
        'moods': ['fear', 'angst', 'serious', 'overworked', 'stormy', 'depressed', 'intense'],
    },
    '#FFFF00': {
        'name': 'yellow',
        'stereotype': ('annoyance', (10, 90)),
        'moods': ['anxious', 'cool', 'cautious', 'distracted', 'mellow', 'so-so']
    },
    '#FFA500': {
        'name': 'orange',
        'stereotype': ('upset', (30, 70)),
        'moods': ['stressed', 'nervous', 'mixed', 'confused', 'upset', 'challenged', 'indignant']
    },
    '#E6E200': {
        'name': 'peridot', # light yellowish green
        'stereotype': ('exasperation', (35, 65)),
        'moods': ['restless', 'irritated', 'distressed', 'worried', 'hopeful']
    },
    '#00755E': {
        'name': 'green',
        'stereotype': ('envy', (40, 60)),
        'moods': ['normal', 'alert', 'sensitive', 'jealous', 'envious', 'guarded']
    },
    '#40E0D0': {
        'name': 'turquoise',
        'stereotype': ('pleasing', (90, 10)),
        'moods': ['upbeat', 'pleased', 'relaxed', 'motivated', 'flirtatious']
    },
    '#4169E1': {
        'name': 'blue',
        'stereotype': ('understanding', (65, 35)),
        'moods': ['normal', 'optimistic', 'accepting', 'calm', 'peaceful', 'pleasant']
    },
    '#12008B': {
        'name': 'indigo',
        'stereotype': ('happiness', (100, 0)),
        'moods': ['relaxed', 'happy', 'lovestruck', 'bliss', 'giving']
    },
    '#8A2BE2': {
        'name': 'violet',
        'stereotype': ('excitement', (70, 30)),
        'moods': ['love', 'romance', 'amorous', 'heat', 'mischievous', 'moody', 'dreamer', 'sensual']
    },
    '#FFC0CB': {
        'name': 'pink',
        'stereotype': ('approval', (100, 0)),
        'moods': ['happy', 'warm', 'affectionate', 'loving', 'infatuated', 'curious']
    }
}        


TOPICS = {
    'war': ['war', 'terrorism', 'attack', 'dead', 'military'], 
    'arts': ['arts', 'painting', 'music', 'acting', 'exhibition'], 
    'environment': ['environment', 'climate', 'vegetation', 'animal', 'organism'], 
    'politics': ['politics', 'legislation', 'government', 'party', 'president'],
}     

TOPIC_VECTORS = {
    'war': np.array([-1, -1, 1]),
    'arts': np.array([1, 1, 1]),
    'environment': np.array([1, -1, 1]),
    'politics': np.array([-1, -1, 1]),
}


def get_closest_mood_color(emotion, model):
    mappings = [(v['stereotype'][0], k) for k,v in mood_colors.items()]
    closest = mappings[0][0]
    sim = model.similarity(emotion, mappings[0][0])
    for m in mappings:
        s = model.similarity(emotion, m[0])
        if s > sim:
            sim = s
            closest = m[1]
    return closest
        
    

class NewAgePersonality():
    '''New age personality traits for given date.
    
    After initialization the object holds current traits of the personality, 
    which can be retrieved with :py:func:`get_mood`-method.
    
    The mood is a dictionary of attributes and values of relevant to the 
    personality. The personality can be used, e.g. to :py:func:`react` to given 
    text, and it can be triggered to alter its mood with :py:func:`change_mood`.
    
    Currently, the mood contains following attributes:
    
    ===========    ============================================        
    Key            Value
    ===========    ============================================
    lunation       Current lunation in [0,1], 0.5 is full moon.
    moon_phase     Current moon phase as a string
    aura_color     Current color of the aura
    emotion        Current main emotion 
    ===========    ============================================
    '''
    
    def __init__(self, date = datetime.date.today()):
        self.date = date
        self.lunation = self._get_phase_on_day(date)
        self.moon_phase = self.__get_phase_string(self.lunation)
        self.aura_color = self.aura_color(self.lunation, date)
        mood_color = cu.get_closest(self.aura_color, mood_colors.keys())
        self.emotion = mood_colors[mood_color[1]]['stereotype'][0]
        
        
    def react(self, text, model):
        '''React to text based on the current mood.
        
        The text is run through several classifiers to get a general picture of
        it. The reaction returned is a new emotion string. The current mood of 
        the personality is not (yet) changed by reaction. 
        
        The text classification analysis is enhanced with searching the the 
        space of possible reactions based on the model. The given model should 
        have ``similarity``-method which takes as an argument two strings and 
        ``n_similarity``-method which takes as an argument two iterables 
        consisting of string. Example of a suitable model is, e.g. 
        `gensim's Word2Vec <http://radimrehurek.com/gensim/models/word2vec.html>`_.
        
        :param text: Text which causes reaction
        :type text: str or unicode
        :param model: Model to search for most suitable reaction.
        :type model: Word2Vec or similar
        :returns: str -- Reaction.
        '''
        point = loevheim_cube.map_stimulation(self.emotion, model)
        bow = bag_of_words(text, counts = True)
        words = map(lambda x: x[0], bow)
        ret = uclass.mood([text])
        mood = ret[0][2]
        topic_vector = self.topic_reaction_vector(model, words, mood)
        values = uclass.values([text])[0][2]
        em = loevheim_cube.get_closest(topic_vector, vector = True)[0]
        return (em, bow[:3], topic_vector)
        
    
    def get_mood(self):
        '''Return current mood as a dictionary.'''
        return {'lunation': self.lunation, 'moon_phase': self.moon_phase,\
                'aura_color': self.aura_color, 'emotion': self.emotion}       

    
    def change_mood(self, date = datetime.date.today()):
        """Change current personality's mood.
        
        Returns changed mood as dictionary with at least following keys:
            
        :param date: Day for the mood. Date affects mood traits, see e.g. :py:func:`get_aura_color`.
        :type date: date
        :returns: dict -- Current mood traits.
        """
        self.lunation = self.get_phase_on_day(date)
        self.moon_phase = self.__get_phase_string(self.lunation)
        self.aura_color = self.aura_color(self.lunation, date)
        mood_color = cu.get_closest(self.aura_color, mood_colors.keys())
        self.emotion = mood_colors[mood_color[1]]['stereotype'][0]
         
        return self.get_mood()
        
        
    def _get_phase_on_day(self, date = datetime.date.today()):
        '''Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new'''
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
    
    def __get_phase_string(self, lunation):
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
        
    def aura_color(self, lunation, date = datetime.date.today()):   
        '''Aura color for given date and lunation. 
        
        .. note::
            
            The lunation's correctness to the date is not checked.
        
        Lunation affects the *a*- and *b*-color opponent dimensions in LAB-color 
        space. Lightness depends on the time of the year. More precisely, 
        ligtness is calculated from how long the sun is above the horizon in 
        Helsinki during the day, i.e. aura colors tend to be darker during the 
        winter.
        
        The exact formulas for *l*, *a* and *b* is::
            
            l = (sun_above_horizon / 24h)*100 + N(0, 40)
            a = sin(2 * PI * lunation)*80 + N(0, 30)
            b = cos(2 * PI * lunation)*80 + N(0, 30),
            
        where *N(0, X)* is normal distribution with zero mean and *X* variance.
        The lightness value is restricted to the interval [20, 100].     
        '''
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
        angle = 2 * math.pi * lunation - (0.5 * math.pi)
        a = math.sin(angle) * 80
        b = math.cos(angle) * 80
        return (a, b)
    
    
    def topic_reaction_vector(self, model, bow, mood):
        '''Calculate sum vector for reactions to all topics.
        
        :param model: Model to analyze bow and topic similarities
        :type model: Word2Vec or similar
        :param bow: bag-of-words extracted from original text
        :type bow: iterable
        :param mood: Mood extracted from original text, happy-upset ratio.
        :type mood: tuple
        '''
        topic_sims = self.__analyse_topics(model, bow) 
        polarized = True if abs(float(mood[0][1]) - float(mood[1][1])) > 0.3 else False
        happy = True if float(mood[0][1]) > 0.5 else False
        vectors = {}
        for k,v in TOPIC_VECTORS.items():
            vectors[k] = v           
        if polarized and happy:
            vectors['war'] = vectors['war'] * -1
            vectors['politics'] = vectors['politics'] * -1
        if polarized and not happy:
            vectors['arts'] = vectors['arts'] * -1
            vectors['environment'] = vectors['environment'] * -1
        vector = np.array([0, 0, 0])
        for k, v in topic_sims.items():
            vector = vector + vectors[k]*v
        return self.__normalize(vector)    
        
    
    def __analyse_topics(self, model, bow):
        sims = self.__topic_similarities(model, TOPICS, bow)
        smax = max(sims.values()) # sims in [0, 1]
        sadj = 1.0 / smax
        for k,v in sims.items():
            sims[k] = (sadj * v) ** 2        
        return sims
        
    
    def __topic_similarities(self, model, topics, bow):
        fbow = []
        for w in bow:
            try:
                model.similarity('man', w)
            except:
                continue
            fbow.append(w)
        sims = {}
        for k, v in topics.items():
            sims[k] = model.n_similarity(v, fbow)
        return sims
    
    
    def __normalize(self, v):
        return v / self.__ed((0,0,0), v)
    
    def __ed(self, p1, p2):
        ps = zip(p1, p2)
        return np.sqrt(reduce(lambda x,y: x+abs(y[0] - y[1])**2, ps, 0))
    
    
    def _test_topic_reactions(self, model, plot = False):
        from web import rss
        article_maps = {}
        print "Getting articles from feeds... ",
        sys.stdout.flush()
        for feed, url in rss.REUTERS_RSS_FEEDS.items():
            print feed.upper() + ", ",
            sys.stdout.flush()
            ret = rss.get_articles(url, amount = 3)
            for r in ret:
                em, nn, vector = self.react(r['text'], model)
                article_maps[feed.upper() + ": " + r['title']] = (em, nn, vector)
        print "done."
        titles = []
        X = []
        Y = []
        Z = []
        import interjections
        for k,val in article_maps.items():
            em, nn, v = val
            titles.append(k)
            X.append(v[0])
            Y.append(v[1])
            Z.append(v[2])
            #em = loevheim_cube.get_closest(v, vector = True)[0]
            ws = reduce(lambda x,y: x + " " + y[0], nn, "")
            ret = interjections.get(em.lower(), model)
            if ret is not None:
                interjection, base = ret
            else:
                interjection = ""
            print u"{:<16} -- {:<10} -- {:<35} -- {}".format(em.upper(), interjection, ws, k)
               
        if plot:        
            loevheim_cube.plot_emotions(titles, X, Y, Z)
            

