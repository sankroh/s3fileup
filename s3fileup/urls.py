from django.conf.urls import patterns, include

from tastypie.api import Api
from s3fileup.api.resources import S3PutResource

v1_api = Api(api_name='v1')
v1_api.register(S3PutResource())

urlpatterns = patterns('',
    (r'^s3/', include(v1_api.urls)),
)
