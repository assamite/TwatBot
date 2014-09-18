Installing
==========

TwatBot is developed as a `Django <https://djangoproject.com/>`_ app and uses 
Twitter app API, so you need to apply for application keys from Twitter in 
order to use this project.

Short installing notes:

* Install `pip <https://pypi.python.org/pypi/pip>`_
* Install third party libraries::

	$> cd project_root/
	$> pip install -r requirements.txt # you might need root priviledges
	
* Set local settings for accessing Twitter API::

	$> cd project_root/TwatBot/
	$> touch lsettings.py
	
* Populate ``lsettings.py``  with at least following attributes (see Twitter API documentation for details)::

	TWITTER_API_KEY = 'Your Twitter API key'
	TWITTER_API_SECRET  = 'Your Twitter API secret'
	TWITTER_ACCESS_TOKEN = 'Your Twitter access token'
	TWITTER_ACCESS_TOKEN_SECRET = 'Your Twitter access token secret'


