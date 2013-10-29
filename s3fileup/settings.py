from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


GENERATE_BUCKET = getattr(settings, 'S3FILEUP_GENERATE_BUCKET', False)
BUCKET_PREFIX = getattr(settings, 'S3FILEUP_BUCKET_PREFIX', None)

if GENERATE_BUCKET and BUCKET_PREFIX is None:
    raise ImproperlyConfigured('You have to specify BUCKET_PREFIX, in settings.py, if you want to generate a bucket.')

BUCKET_NAME = getattr(settings, 'S3FILEUP_BUCKET_NAME', None)

if not GENERATE_BUCKET and BUCKET_NAME is None:
    raise ImproperlyConfigured('You have to specify BUCKET_NAME, in settings.py, in order to generate an upload URL.')

DOMAIN = getattr(settings, 'S3FILEUP_DOMAIN', None)

if DOMAIN is None:
    raise ImproperlyConfigured('You have to specify a DOMAIN_NAME, in settings.py')

MAX_AGE = getattr(settings, 'S3FILEUP_MAX_AGE', 3000)
