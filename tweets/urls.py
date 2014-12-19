"""
.. py:module:: `urls`
    :platform: Unix
    
Custom URLs for tweets-app.   
"""
from django.conf.urls import patterns, include, url
from views import (
    home, 
    blend, 
    names, 
    tweets, 
    aura_color, 
    mood_color_test, 
    interjection_test,
    monkey_test,
    image_search_test,
)

urlpatterns = patterns('',
    url(r'^$', home, name='tweets_home_url'),
    url(r'^blend$', blend, name='tweets_blend_url'),
    url(r'^names$', names, name='tweets_names_url'),
    url(r'^tweets/(?P<num>.*)$', tweets, name='tweets_tweets_url'),
    url(r'^aura$', aura_color, name='tweets_aura_url'),
    url(r'^emotion/(?P<category>.*)$', mood_color_test, name='tweets_mood_color_urls'),
    url(r'^reaction/(?P<category>.*)$', interjection_test, name='tweets_reaction_urls'),
    url(r'^monkey/(?P<num>.*)$', monkey_test, name = 'tweets_monkey_url'),
    url(r'^image_search/(?P<emotion>.*)$', image_search_test, name = 'tweets_image_search_url')
)
