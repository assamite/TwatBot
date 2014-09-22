"""
.. py:module:: `urls`
    :platform: Unix
    
Custom urls for tweets-app.   
"""
from django.conf.urls import patterns, include, url
from views import home

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TwatBot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name='twatbot_home_url'),
)
