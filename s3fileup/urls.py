from django.conf.urls import patterns, include, url

urlpatterns = patterns('s3fileup.views',
    url(r'^s3put/$', 'put_url', name='s3fileup:put_url'),
    url(r'^s3get/$', 'get_url', name='s3fileup:get_url'),
)
