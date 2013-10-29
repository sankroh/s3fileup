import datetime
import os

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.cors import CORSConfiguration
from boto.exception import S3CreateError
from django.core.exceptions import ImproperlyConfigured

from .settings import GENERATE_BUCKET, BUCKET_PREFIX, BUCKET_NAME, DOMAIN, \
                    MAX_AGE


def generate_bucket_name():
    """
    TODO: Generate custom bucket name
    """
    if GENERATE_BUCKET:
        bucket_prefix = BUCKET_PREFIX
        bucket_name = '{0}_{1}'.format(bucket_prefix, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M'))
    else:
        bucket_name = BUCKET_NAME
    return bucket_name


def generate_signed_url(obj_name, obj_type, method='GET'):
    """
    This method generates a temporary URL for an object in S3
    """
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None:
        raise ImproperlyConfigured('You need to specify AWS access keys!')

    conn = S3Connection(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        calling_format=OrdinaryCallingFormat()
    )

    bucket_name = generate_bucket_name()

    try:
        bucket = conn.create_bucket(bucket_name)
        is_new = True
    except S3CreateError:
        bucket = conn.lookup(bucket_name)
        is_new = False

    if method in ('PUT', 'POST') and is_new:
        # Setting CORS config (Cross Origin Resource)
        cors_cfg = CORSConfiguration()
        cors_cfg.add_rule(['PUT', 'POST', 'DELETE'], DOMAIN, allowed_header='*', max_age_seconds=3000, expose_header='x-amz-server-side-encryption')
        cors_cfg.add_rule('GET', '*')
        bucket.set_cors(cors_cfg)

    headers= {
        'Content-Type': obj_type,
        'x-amz-acl' : 'public-read',
    }

    url = conn.generate_url(MAX_AGE, method, bucket=bucket_name, key=obj_name, headers=headers)

    return url
