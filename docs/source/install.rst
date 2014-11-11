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

* Clone (or fork) project's git-repository::

	$> git clone https://github.com/assamite/TwatBot.git

* Install `pip <https://pypi.python.org/pypi/pip>`_
* Install third party libraries::

	$> cd project_root/
	$> pip install -r requirements.txt // you might need root privileges
	
* From dependencies, `nltk <http://www.nltk.org/>`_-package needs wordnet and `textblob <https://textblob.readthedocs.org/en/dev/>`_ some other corporas to be able to function. You can download them using following commands::
	
	$>python -m textblob.download_corpora
	$>python -c "import nltk; nltk.download()"
	
* Install `MySQL <http://www.mysql.com/>`_ and create MySQL database::

	$>mysql -u root -p
	mysql> create database your_db_name character set 'utf8' collate 'utf8_general_ci';
	mysql> grant usage on *.* to your_user@localhost identified by 'your_user_password';
	mysql> grant all privileges on your_db_name.* to your_user@localhost ;	
	
* Create local settings file::

	$> cd project_root/TwatBot/
	$> touch lsettings.py
	
* Configure ``lsettings.py``  with at least following attributes (see Twitter API documentation for details)::

	SECRET_KEY = 'Secret key for Django'
	TWITTER_API_KEY = 'Your Twitter API key'
	TWITTER_API_SECRET  = 'Your Twitter API secret'
	TWITTER_ACCESS_TOKEN = 'Your Twitter access token'
	TWITTER_ACCESS_TOKEN_SECRET = 'Your Twitter access token secret'
	DATABASE = 'your_db_name'
	USER = 'your_user'
	PASSWORD = 'your_user_password'

* Create DB-tables and apply migrations::
	
	$> cd project_root/
	$> python manage.py syncdb
	$> python manage.py migrate django_cron
	$> python manage.py migrate tweets
	
* Populate ``tweets``-app models with initial data::	

	$> python manage.py loaddata tweets/fixtures/fixtures.json
	
* Configure project's cronjobs to be run every 5 minutes (or so)

	.. warning::
		This will make your bot to Tweet every once in a while, so only do this
		when you are ready to face the consequences.
		
		**If you just want to test the bot locally, don't enable cronjobs.**

	* Open crontab in new editor from terminal::

		$> env EDITOR=nano crontab -e
		
	* Write the cronjob on new line (you need to change the paths to your bash profile and project)::
	
		*/5 * * * * source ~/.bash_profile && python path/to/TwatBot/manage.py runcrons > path/to/TwatBot/logs/cronjob.log
		
	* Save and exit. Now the terminal should say something like::
	
		crontab: installing new crontab
	
**Local Usage:**
	
* Run the Django's builtin test server::

	$> python manage.py runserver
	
* Now the web site should be served for you in ``127.0.0.1:8000/``
	



