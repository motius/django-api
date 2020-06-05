from .base import *
from socket import gethostname, gethostbyname

ALLOWED_HOSTS = ["localhost", gethostname(), gethostbyname(gethostname()), os.environ.get('SITE_URL')]

DEBUG = True

SITE_URL = '{}://{}'.format(os.environ.get('SITE_PROTOCOL', 'http'), os.environ.get('SITE_URL'))
STATIC_URL = '{}://{}/static/'.format(os.environ.get('SITE_PROTOCOL','http'), os.environ.get('SITE_URL'))

CORS_ORIGIN_ALLOW_ALL = True

try:
    from .local import *
except ImportError:
    pass
