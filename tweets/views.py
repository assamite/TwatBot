"""
.. py:module:: views
    :platform: Unix
    :synopsis: Views for Django app.
        
Custom views for the app for testing and publishing new tweets.
"""
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from tweets import COLOR_SEMANTICS as semantics


def home(request):
    """Basic view to be implemented.
    """ 
    context = RequestContext(request)
    return render_to_response('home.html', context)


def blend(request):
    """Test blending of splitted unigrams."""
    ret = semantics.blend_all_unigram_splits(a_head = 0.7)
    blends = []
    for r in ret:
        h, m = r[0]
        ch, cm, cb = r[1]
        blends.append({'head': h, 'modifier': m, 'head_color': ch, 'modifier_color': cm, 'blended_color': cb})
    context = RequestContext(request, { 'blends': blends })
    return render_to_response('blend_test.html', context)
    
    
    