"""
.. py:module:: views
    :platform: Unix
    :synopsis: Views for Django app.
        
Custom views for the app for testing and publishing new tweets.
"""
import random

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from tweets.core import TWEET_CORE


def home(request):
    """Basic view to be implemented.
    """ 
    context = RequestContext(request)
    return render_to_response('home.html', context)


def blend(request):
    """Test blending of splitted unigrams."""
    from tweets.core import COLOR_SEMANTICS as semantics
    ret = semantics.blend_all_unigram_splits(a_head = 0.60)
    blends = []
    for r in ret:
        h, m = r[0]
        ch, cm, cb = r[1]
        blends.append({'head': h, 'modifier': m, 'head_color': ch, 'modifier_color': cm, 'blended_color': cb})
    context = RequestContext(request, { 'blends': blends })
    return render_to_response('blend_test.html', context)


def names(request):
    """Test color names for the everycolorbot tweets."""
    from tweets.core import COLOR_SEMANTICS as semantics
    from models import EveryColorBotTweet
    objects = EveryColorBotTweet.objects.all()
    names = []
    samples = random.sample(objects, 10)
    for o in samples:
        n = semantics.get_knn_blended_unigrams(o.color.html, k = 4)
        names.append({'color': o.color.html, 'url': o.url, 
                      'c1': n[0][1], 'n1': n[0][2][0] + n[0][2][1],
                      'c2': n[1][1], 'n2': n[1][2][0] + n[1][2][1],
                      'c3': n[2][1], 'n3': n[2][2][0] + n[2][2][1],
                      'c4': n[3][1], 'n4': n[3][2][0] + n[3][2][1]
        })
        
    context = RequestContext(request, {'names': names})
    return render_to_response('names_test.html', context)
        
    
def tweets(request, num = 1):
    """Test tweeting functionality."""   
    tweets = []
    for i in xrange(int(num)):
        ret = TWEET_CORE.tweet(send_to_twitter = False)
        if ret.tweet:
            tweet = ret.tweet
            color_code = ret.color_code
            value = ret.appreciation
            tweets.append({'tweet': tweet, 'color_code': color_code, 'value': value})
        
    context = RequestContext(request, {'tweets': tweets})
    return render_to_response('tweets_test.html', context)
    
    
def aura_color(request):
    import numpy as np
    import datetime
    from new_age import NewAgePersonality as NAP
    from tweets.utils import color
    nap = NAP()
    date = datetime.date.today()
    auras = []
    for i in xrange(365):
        ret = nap.get_mood(date)
        ac = color.rgb2html(ret['aura_color'])
        phase = ret['moon_phase']
        lunation = ret['lunation']
        auras.append({'color_code': ac, 'date': date, 'moon_phase': phase, 'lunation': lunation })
        date += datetime.timedelta(1, 0)
    
    context = RequestContext(request, {'auras': auras})
    return render_to_response('aura_test.html', context)
    
    