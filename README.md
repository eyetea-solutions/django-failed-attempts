# django-failed-attempts

Django application for blocking users with too many authentication failed attempts. The actual blocking is time based and blocks USER and IP unique combination. 

This project is fork from BruteBuster. The original project is started by Cyber Security Consulting .

Visit http://code.google.com/p/django-brutebuster/ for early versions

## Installation

* Add the django application in the project directory.

* Add django_failed_attempts to installed APPS in settings.py

* Add variable AUTH_PROTECTION_BACKEND that holds your authentication backend.
AUTH_PROTECTION_BACKEND= 'django.contrib.auth.backends.ModelBackend'

* Replace the default authentication backends to be the django_failed_attempts in settings.py. 
AUTHENTICATION_BACKENDS = (
	'django_failed_attempts.backends.FailedAttemptBackend',
)
* Add variables in settings.py to override the default settings for blocking.
BB_MAX_FAILURES = 5
BB_BLOCK_INTERVAL = 15
