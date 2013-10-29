from django.conf.urls import patterns, include, url

from s3fileup.api.views import generate_s3_url


urlpatterns = patterns('',
    url(r'^s3/s3put/', generate_s3_url, name='s3fileup:s3-upload-url'),
)
