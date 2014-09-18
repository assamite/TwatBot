TwatBot
==========

TwatBot is a twitter bot built for a course "Computational foundations of linguistic creativity",
held in University of Helsinki, fall 2014.

TwatBot generates color names for color codes, e.g. ``0x081960``, based on the 
linguistic knowledge it has on different colors, and their relations. The project 
is developed as a Django app, so that its reasoning for giving certain names to 
certain color codes is easy to follow from a web site.


Weekly reports
-----------------
Here are some comments on weekly development during the course.

Week 2
****************
I have made some color utilities into the ``colorbot/color_utilities.py``, and
added Django models for the resources given on the course. Otherwise
the project is still a clean Django-project skeleton. The documentation of
the project can be found `here <http://assamite.github.io/TwatBot>`_. 

Most of my week's work went to setting up and learning Sphinx (and how to hook it to be
nearly automatically served in github pages) as I haven't used it before, and now 
seemed like a good time to start using it!


