import datetime

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.cors import CORSConfiguration
from boto.exception import S3CreateError
from django.conf import settings


def generate_bucket_name():
    """
    TODO: Generate custom bucket name
    """
    if settings.S3FILEUP_GENERATE_BUCKET:
        bucket_prefix = settings.S3FILEUP_BUCKET_PREFIX
        bucket_name = '{0}_{1}'.format(bucket_prefix, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M'))
    else:
        bucket_name = settings.S3FILEUP_BUCKET_NAME
    return bucket_name


def generate_signed_url(obj_name, obj_type, method='GET'):
    """
    This method generates a temporary URL for an object in S3
    """
    # Maybe do some error handling here
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    conn = S3Connection(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        calling_format=OrdinaryCallingFormat()
    )

    bucket_name = generate_bucket_name()

    try:
        bucket = conn.create_bucket(bucket_name)
    except S3CreateError:
        bucket = conn.lookup(bucket_name)

    if method in ('PUT', 'POST'):
        # Setting CORS config (Cross Origin Resource)
        cors_cfg = CORSConfiguration()
        cors_cfg.add_rule(['PUT', 'POST', 'DELETE'], settings.S3FILEUP_DOMAIN, allowed_header='*', max_age_seconds=3000, expose_header='x-amz-server-side-encryption')
        cors_cfg.add_rule('GET', '*')
        bucket.set_cors(cors_cfg)

    headers= {
        'Content-Type': obj_type,
        'x-amz-acl' : 'public-read',
    }

    url = conn.generate_url(300, method, bucket=bucket_name, key=obj_name, headers=headers)

    return url
