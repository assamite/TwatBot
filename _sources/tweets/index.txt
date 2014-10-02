Tweets Module
================

.. toctree::
	:hidden:
	
	core
	muses
	framing
	contexts
	color_semantics
	color_utils
	resources_utils
	models
	views
	
	
Main package of the project, developed as a Django app. It has currently following modules.

* **Django App Modules:**

	* :py:mod:`models`: Django models for resources given on the course.
	* :py:mod:`views`: Custom Django views for the app.
	* :py:mod:`urls`: Custom urls for the app.
	* :py:mod:`admin`: Django admin functions.
	* :py:mod:`tests`: Basic tests for the app.

* **Modules Explicitly Made For TwatBot:**

	* :py:mod:`core`: Core of the color tweets. Glues other modules' functionality together.
	* :py:mod:`muses`: Muses for the tweets, i.e. sources for color codes.
	* :py:mod:`framing`: Framing of the color tweets
	* :py:mod:`contexts`: Different contexts for framing
	* :py:mod:`color_semantics`: Semantically informed color manipulations
	* :py:mod:`color_utils`: Semantic ignorant color utility functions
	* :py:mod:`resources_utils`: Functions to populate Django models with contents in ``resources/``
