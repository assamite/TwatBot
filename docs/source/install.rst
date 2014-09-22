Installing
==========

TwatBot is developed as a `Django <https://djangoproject.com/>`_ app. Access to 
`Twitter API <https://dev.twitter.com/overview/documentation>`_ is gained using 
`python-twitter <https://pypi.python.org/pypi/python-twitter/2.0>`_.

You should be familiar with basic Django project layout and have a working 
`Twitter app <https://apps.twitter.com/>`_ which allows you to tweet before 
using this project.

Short installing notes:

* Install `pip <https://pypi.python.org/pypi/pip>`_
* Install third party libraries::

	$> cd project_root/
	$> pip install -r requirements.txt // you might need root privileges
	
* Create local settings file::

	$> cd project_root/TwatBot/
	$> touch lsettings.py
	
* Configure ``lsettings.py``  with at least following attributes (see Twitter API documentation for details)::

	SECRET_KEY = 'Secret key for Django'
	TWITTER_API_KEY = 'Your Twitter API key'
	TWITTER_API_SECRET  = 'Your Twitter API secret'
	TWITTER_ACCESS_TOKEN = 'Your Twitter access token'
	TWITTER_ACCESS_TOKEN_SECRET = 'Your Twitter access token secret'
	
* Create DB-tables and populate ``tweets``-app models with premade information::
	
	$> cd project_root/
	$> python manage.py syncdb
	$> cd tweets/
	$> python resources_utils.py
	



