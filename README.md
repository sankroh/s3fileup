django-s3fileup
===============

Overview
--------

S3FileUp is an Apache2 Licensed pluggable Django app that provides you with an
API to upload files to S3 directly from the browser, without the file ever
touching your server.

3rd Party Requirements
----------------------
boto==2.7.0
django-tastypie==0.9.11


Installation
------------

Install using pip, this will install the 3rd party libs required as well:

    pip install s3fileup

Add to settings.INSTALLED_APPS:

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        ...
        'django.contrib.sites',

        # Add here.
        's3fileup',

        # Then your usual apps.
        'blog',
    )

Hook up the URLs, add this to your URLConf:

    (r'^uploads/', include('s3fileup.urls')),


Settings
--------

# TODO Add settings used


Usage
-----

This app exposes two URLs that can be used by the client. Using the example
above, the endpoints are ``/uploads/s3/v1/s3put/`` and ``/uploads/s3/v1/s3get``.
