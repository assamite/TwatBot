Code Layout
===============

Basic structure of the project's code follows modern Django project's layout::

	project_root/	
		manage.py        -- Django's management module
		README.rst       -- Readme for Github
		requirements.txt -- requirements for pip installation

		TwatBot/
			__init__.py
			settings.py  -- Django settings
			lsettings.py -- User created local settings
			urls.py      -- Root url-config for Django
			wsgi.py	     -- Django module for wsgi
			
		tweets/
			-- main app of the project, see package's documentation	
			fixtures/
				-- initial data dumps, created from pregiven resources		
		resources/
			-- pregiven resources for the project		
		docs/
			-- Sphinx documentation source files
				
			
			
		