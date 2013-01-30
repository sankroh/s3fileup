===============
django-tastypie
===============

Overview
--------

S3FileUp is an Apache2 Licensed pluggable Django app that provides you with an
API to upload files to S3 directly from the browser, without the file ever
touching your server.

Installation
------------

Install using pip, this will install the 3rd party libs required as well:

    pip install s3fileup

Add to settings.INSTALLED_APPS:

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',

        # Add here.
        's3fileup',

        # Then your usual apps...
        'blog',
    )

Hook up the URLs, add this to your URLConf:

    (r'^uploads/', include('s3fileup.urls')),


Usage
-----
