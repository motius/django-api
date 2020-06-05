from .base import *

DEBUG = False

ALLOWED_HOSTS = ["localhost", os.environ.get('SITE_URL')]

SITE_URL = 'https://{}'.format(os.environ.get('SITE_URL'))
STATIC_URL = 'https://{}/static/'.format(os.environ.get('SITE_URL'))

CORS_ORIGIN_ALLOW_ALL = True  # TODO: Update CORS for the final production URL and disable this

try:
    from .local import *
except ImportError:
    pass
