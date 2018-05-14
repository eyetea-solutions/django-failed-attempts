from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend 
from django_failed_attempts.models import FailedAttempt
from django.conf import settings
from django.core.exceptions import ValidationError
from importlib import import_module


AUTH_PROTECTION_BACKEND = settings.AUTH_PROTECTION_BACKEND.split('.')
AUTH_PROTECTION_CLASS = str(AUTH_PROTECTION_BACKEND[-1])
AUTH_PROTECTION_MODULE = str(('.').join(AUTH_PROTECTION_BACKEND[:len(AUTH_PROTECTION_BACKEND)-1]))

auth_backend = getattr(import_module(AUTH_PROTECTION_MODULE), AUTH_PROTECTION_CLASS)

UserModel = get_user_model()

LOCKOUT_MESSAGE = getattr(
    settings,
    'BB_LOCKOUT_MESSAGE',
    'You are locked out. Please try again later or '
    'contact support for assistance.'
)

class FailedAttemptBackend(auth_backend):
    def authenticate(self, request, username=None, password=None, **kwargs):    
        
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        # Call the authenticate function from the parent class
        result = super().authenticate(request, username, password, **kwargs)

        if request:
            # try to get the remote address from thread locals
            # First check if the client IP is captured in a different header
            # by a forwarding proxy.
            ip_list = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')
            IP_ADDR = ip_list[0].strip()
            if not IP_ADDR:
                # Otherwise, use the basic REMOTE_ADDR header.
                IP_ADDR = request.META.get('REMOTE_ADDR', None)
        else:
            IP_ADDR = None
        
        try:
            fa = FailedAttempt.objects.filter(username=username, IP=IP_ADDR)[0]
            if fa.recent_failure():
                if fa.too_many_failures():
                    # we block the authentication attempt because
                    # of too many recent failures
                    fa.failures += 1
                    fa.save()
                    # Raise validation error
                    raise ValidationError(LOCKOUT_MESSAGE)
            else:
                # the block interval is over, so let's start
                # with a clean sheet
                fa.failures = 0
                fa.save()
        except IndexError:
            # No previous failed attempts
            fa = None
            
        if result:
            # the authentication was successful - we do nothing
            return result
    
        fa = fa or FailedAttempt(username=username, IP=IP_ADDR, failures=0)
        fa.failures += 1
        fa.save()

        return None
        
