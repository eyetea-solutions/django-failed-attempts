# django-failed-attempts

Django application for blocking users with too many authentication failed attempts. The actual blocking is time based and blocks USER and IP unique combination. 

This project is fork from BruteBuster. The original project is started by Cyber Security Consulting .

Visit http://code.google.com/p/django-brutebuster/ for early versions

## Installation

* Add the django application in the project directory.
* Add django_failed_attempts to installed APPS in settings.py
* Add variable AUTH_PROTECTION_BACKEND = 'django.contrib.auth.backends.ModelBackend'
* Replace the default authentication backends in settings.py with 'django_failed_attempts.backends.FailedAttemptBackend'
