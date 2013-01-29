import os

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.cors import CORSConfiguration
from boto.exception import S3CreateError
from django.conf import settings

from tastypie import fields, utils
from tastypie.resources import Resource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization


class S3PutResource(Resource):
    url = fields.CharField(attribute='url', blank=True)
    error = fields.CharField(attribute='error', blank=True)

    class Meta:
        allowed_methods = ['post']
        always_return_data = True
        authorization = Authorization()
        #authentication = BasicAuthentication()
        resource_name = 's3put'


    def _generate_bucket_name(self):
        """
        TODO: Generate custom bucket name
        """
        AWS_STORAGE_BUCKET_NAME = 'app_mi_assets'
        return AWS_STORAGE_BUCKET_NAME


    def _generate_signed_url(self, obj_name, obj_type, method='GET'):
        """
        This method generates a temporary URL for an object in S3
        """
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

        conn = S3Connection(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            calling_format=OrdinaryCallingFormat()
        )

        bucket_name = self._generate_bucket_name()
        try:
            bucket = conn.create_bucket(bucket_name)
        except S3CreateError:
            bucket =conn.lookup(bucket_name)

        if method in ('PUT', 'POST'):
            # Setting CORS config (Cross Origin Resource)
            cors_cfg = CORSConfiguration()
            cors_cfg.add_rule(['PUT', 'POST', 'DELETE'], 'http://localhost:5000', allowed_header='*', max_age_seconds=3000, expose_header='x-amz-server-side-encryption')
            cors_cfg.add_rule('GET', '*')
            bucket.set_cors(cors_cfg)

        headers= {
            'Content-Type': obj_type,
            'x-amz-acl' : 'public-read',
        }

        url = conn.generate_url(300, method, bucket=bucket_name, key=obj_name, headers=headers)

        return url

    def post_list(self, request, **kwargs):
        s3_object_type = request.POST.get('s3_object_type', 'application/octet-stream')
        s3_object_name = request.POST.get('s3_object_name', None)

        if None in (s3_object_type, s3_object_name):
            raise HttpBadRequest()

        url = self._generate_signed_url(s3_object_name, s3_object_type, method='PUT')

        result = { 'url' : url }
        return self.create_response(request, result)

