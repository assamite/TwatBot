Tweets Package
================

.. toctree::
	:hidden:
	:maxdepth: 5
	
	core
	muses
	contexts
	color_semantics
	reasoning
	new_age
	interjections
	models
	views
	web/index
	utils/index
	
	
Main package of the project, developed as a Django app. The app has currently following modules.

* **Django App Modules:**

	* :py:mod:`models`: Django models for resources given on the course.
	* :py:mod:`views`: Custom Django views for the app.
	* :py:mod:`urls`: Custom urls for the app.
	* :py:mod:`admin`: Django admin functions.
	* :py:mod:`tests`: Basic tests for the app.

* **Modules Explicitly Made For TwatBot:**

	* :py:mod:`core`: Core of the color tweets. Glues other modules' functionality together.
	* :py:mod:`muses`: Muses for the tweets, i.e. sources for color codes.
	* :py:mod:`contexts`: Different contexts for framing
	* :py:mod:`color_semantics`: Semantically informed color manipulations
	* :py:mod:`reasoning`: Reasoning for the generated tweets.
	* :py:mod:`new_age`: New Age personality for the tweets
	

General Functionality
---------------------

General functionality and data flow of the package starts from the :py:mod:`core` -module.
It gathers and unifies other modules' functionality together and also acts
as a jury which allows or does no allow tweets to be made. Other modules provide
partial contents and act in different roles in the building of the tweets.

*Muses*

	Muses are the sources of the inspiration for the TwatBot. In essence, they are
	sources which generate color codes on demand. However, they are not restricted 
	to only provide color codes, but can also give various framing -- or other --
	information of the inspiration source, e.g. images, attitudes and such.

*Contexts*

	Contexts provide framings for the tweets. They generate actual tweet contents
	and should be versatile enough in their own right to prohibit meaningless 
	repetition in the tweets. Good contexts accept and use different resources given
	by the muses.

*Color Semantics*

	The main functionality of the color semantics is to provide name suggestions for 
	the color codes -- with an idea how good the matching is -- provided by the muses. 
	The contexts use these name suggestions in generating the suggestions for the 
	tweets contents.

*Core*

	Core glues together color code - color name - context mappings and evaluates if 
	they are good enough to be tweeted. It also compares given color codes and contexts
	to last tweets in memory (to be implemented) so that TwatBot does not appear to be
	too repetitive.






	

