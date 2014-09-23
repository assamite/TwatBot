Tweets
================

.. toctree::
	:hidden:
	
	models
	views
	color_utils
	resources_utils
	color_semantics

Main package of the project, developed as a Django app. It has currently following modules.

* **Django App Modules:**

	* :py:mod:`models`: Django models for resources given on the course.
	* :py:mod:`views`: Custom Django views for the app.
	* :py:mod:`urls`: Custom urls for the app.
	* :py:mod:`admin`: Django admin functions.
	* :py:mod:`tests`: Basic tests for the app.

* **Modules Explicitly Made For TwatBot:**

	* :py:mod:`color_utils`: Semantic ignorant color utility functions
	* :py:mod:`resources_utils`: Functions to populate Django models with contents in ``resources/``
	* :py:mod:`color_semantics`: Semantically informed color manipulations.