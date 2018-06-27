# QPgenerator
generates a random question paper from a database of questions

project requirements:

1 python3 , django 2.0
2 python mysql client
3 django-widget-tweaks
4 weasyprint
5 python-decouple




Project Structure:

QPgenerator
	--qp_generator
		--migrations(contains all database migrations)
		--templates(contains html templates)
			--ajax
			--email(contains templates for email sent by app)
			--include(contains form rendering template)
			--registration(contains all authentication templates)
		--models.py
		--views.py(contains all non ajax views)
		--ajax_views.py(contains all ajax views)
		--urls.py(contains all urls specific to app)
		--forms.py
		--tests
	--QPgenerator
		--media
			--questions(contains question images)
			--match(contains match images)
			--tmp(contains generated papers pdf)
		--settings.py(contains the settings of the project)
		--urls.py(contains urls for the whole project ie, /admin and /app)
		--wsgi.py(config for wsgi)
	--static(put any static files here)
	--staticfiles(static files are collected here by running collectstatic; apache serves static files from here)
	--manage.py
	--.env(contains sensitive env settings we use python decouple import these into settings.py)


django commands(all commands to be executed with prefix python3 manage.py):

1. runserver portno(optional) -- runs django development server
2. makemigrations -- creates migrations to be run on database should be run if any changes are made to models
3. migrate -- run the migrations created by makemigrations
4. collectstatic -- collects all static files from static and other places into staticfiles(the path defined as STATIC_ROOT IN settings.py; can be changed) 
5. createsuperuser creates a superuser(can access django admin)

change of url routes:
	
	if url routes are changed the changes need to be made in qp_generator/urls.py and QPgenerator/urls.py as required.
	Also the following files have hard coded urls which may need to be updated:
	1.settings.py
		---1. MEDIA_URL (this is the url the app prefixes to all requests made to the server for media files)
		---2. STATIC_URL (this is the url the app prefixes to all requests made to the server for static files)
		---3.LOGIN_REDIRECT_URL
		---4.LOGOUT_REDIRECT_URL
		---5.LOGIN_URL
	2.static/js/*
		--- some of the js files have ajax calls with hard coded urls after updtating them run collectstatic and make sure the changes are updated in staticfiles/js/* too.

storage and retrival of static and media files:

1. static files are collected by collectstatic into the path specified in STATIC_ROOT
2. media files(images) are uploaded by the app into the path specified in MEDIA_ROOT
3. In ajax_views.py, to_pdf view the first path specified in html.writepdf() is where the file will be stored.
4. Aso make sure the CSS path specified by the writepdf() is correct.

EMAIL and DATABASE settings can be found in settings.py

NOTE :- all templates inherit from base.html. the blocks in base.html like block content for example will be replaced with the corresponding block in each template when they are rendered.
The nav bar is present in base.html
The Footer is present in home.html,generate_test.html,manage_questions.html

Permissions:
1 each school has admin and teacher users.
2 teachers can view questions and generate papers but cannot create/edit questions or chapters
3 school admins can create and edit chapters and questions
4 Any user created through the signup form will be a teacher user and school password is needed to create such a user
5 Only Django admin can create new schools, grades, subjects and school admin users
6 Django admin is accessible from /qp_gen/admin only to superusers ie users with staff status
7 there are two ways to create superusers:1 from the django admin (check the staff status and superuser check boxes while creating a new user)(Recommended)
										  2 from command line using createsuperuser
8 superusers can perform CRUD operations on all models using django admin


changing permissions for views:
access control to the views is specified using the decorators @login_required, @user_is_admin on top of the view functions in views.py and ajax_views.py they can be changed by adding or removing the decorators as necessary


