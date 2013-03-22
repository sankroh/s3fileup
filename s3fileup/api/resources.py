import os

from tastypie import fields, utils
from tastypie.resources import Resource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization

from s3fileup.utils import generate_signed_url


class S3PutResource(Resource):
    url = fields.CharField(attribute='url', blank=True)
    error = fields.CharField(attribute='error', blank=True)

    class Meta:
        allowed_methods = ['post']
        always_return_data = True
        authorization = Authorization()
        #authentication = BasicAuthentication()
        resource_name = 's3put'


    def post_list(self, request, **kwargs):
        s3_object_type = request.POST.get('s3_object_type', 'application/octet-stream')
        s3_object_name = request.POST.get('s3_object_name', None)

        if None in (s3_object_type, s3_object_name):
            raise HttpBadRequest()

        url = generate_signed_url(s3_object_name, s3_object_type, method='PUT')

        result = { 'url' : url }
        return self.create_response(request, result)

