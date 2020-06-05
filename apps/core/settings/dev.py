from .base import *  # NOQA

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_URL = 'http://0.0.0.0:8000' #NOSONAR

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

try:
    from .local import *
except ImportError:
    pass
