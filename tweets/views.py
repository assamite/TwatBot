"""
.. py:module:: views
    :platform: Unix
    :synopsis: Views for Django app.
        
Custom views for the app for testing and publishing new tweets.
"""
from django.http import HttpResponse
from tweets import COLOR_SEMANTICS as semantics


def home(request):
    """Basic view to be implemented.
    """
    cm = semantics.color_map

    return HttpResponse(cm.items()[0])


def blend(request):
    """Blend two colors view mock.
    """
    pass