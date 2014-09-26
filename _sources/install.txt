Installing
==========

.. warning::
	TwatBot is currently developed for Python 2.7.x. No compatibility for other 
	Python versions is guaranteed.

TwatBot is developed as a `Django <https://djangoproject.com/>`_ app. Access to 
`Twitter API <https://dev.twitter.com/overview/documentation>`_ is gained using 
`python-twitter <https://pypi.python.org/pypi/python-twitter/2.0>`_.

You should be familiar with basic Django project layout and have a working 
`Twitter app <https://apps.twitter.com/>`_ which allows you to tweet before 
using this project.

**Short installing notes:**

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
	
* Create DB-tables and populate ``tweets``-app models with initial data::
	
	$> cd project_root/
	$> python manage.py syncdb
	$> python manage.py loaddata tweets/fixtures/fixtures.json
	
.. note:: 
	In case the syncdb fails, comment out everything in ``tweets/.__init__.py``
	before running syncdb and remove comments afterwards. Will fix this later.
	
**Local Usage:**
	
* Run the Django's builtin test server::

	$> python manage.py runserver
	
* Now the web site should be served for you in ``127.0.0.1:8000/``
	



