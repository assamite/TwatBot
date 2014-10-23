TwatBot
==========

TwatBot is a twitter bot built for a course "Computational foundations of linguistic creativity",
held in University of Helsinki, fall 2014.

TwatBot generates color names for color codes, e.g. ``0x081960``, based on the 
linguistic knowledge it has on different colors, and their relations. The project 
is developed as a Django app, so that its reasoning for giving certain names to 
certain color codes is easy to follow from a web site.

Project's documentation can be found from `github pages <http://assamite.github.io/TwatBot>`_.

.. warning:: 
	If you have old version of the project, you should probably make a clean 
	install because of the extensive changes, e.g. SQLite to MySQL.

After starting the test server, Everycolorbot colors - new color name matches 
can be found from:

	http://127.0.0.1:8000/names
	
Test tweets can be found from:

	http://127.0.0.1:8000/tweets
	


