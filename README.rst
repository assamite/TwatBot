TwatBot
==========

TwatBot is a twitter bot built for a course "Computational foundations of linguistic creativity",
held in University of Helsinki, fall 2014.

TwatBot generates color names for color codes, e.g. ``0x081960``, based on the 
linguistic knowledge it has on different colors, and their relations. The project 
is developed as a Django app, so that its reasoning for giving certain names to 
certain color codes is easy to follow from a web site.

Project's documentation can be found from `github pages <http://assamite.github.io/TwatBot>`_.


Weekly reports
-----------------
Here are some comments on weekly development during the course.

Week 2
****************
I have made some color utilities into the ``tweets/color_utilities.py``, and
added Django models for the resources given on the course. Otherwise
the project is still a clean Django-project skeleton. Most of my week's work went 
to setting up and learning Sphinx (and how to hook it to be
nearly automatically served in github pages) as I haven't used it before, and now 
seemed like a good time to start using it!

Week 3
****************
I still got quite a lot of technical things to figure out and managed to get only 
the most fundamental things to work. The app should be installable and usable 
by using the install notes in documentation. Currently only one URL with
meaningful content is served after Django's server is started (see install for
details): 

127.0.0.1:8000/blend 

This page should serve all the different color blendings of the unigram splits.
See the documentation for ``tweets.color_semantics.ColorSemantics.blend`` for details about the 
blending operation.

I tested the blending with different settings, but it seems that no single
configuration is good for all the unigrams splits for the blending operation. 
Mostly this has to do with the way the "head" and "modifier" words should be 
selected from the unigram split. Sometimes head should be the first word and 
sometimes the second word.


