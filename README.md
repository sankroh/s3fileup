django-s3fileup
===============

S3FileUp is an Apache2 Licensed pluggable Django app that provides you with an
API to upload files to S3 directly from the browser, without the file ever
touching your server.

3rd Party Requirements
----------------------
* boto==2.7.0
* django-tastypie==0.9.11


Installation
------------

Install using pip, this will install the 3rd party libs required as well:
```bash
    $ pip install django-s3fileup
```
Add to settings.INSTALLED_APPS:
```python
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
```
Hook up the URLs, add this to your URLConf:
```python
    (r'^uploads/', include('s3fileup.urls')),
```

Settings
--------

TODO Add settings used


Usage
-----

This app exposes two URLs that can be used by the client. Using the example
above, the endpoints are ``/uploads/s3/v1/s3put/`` and ``/uploads/s3/v1/s3get/``.

``/uploads/s3/v1/s3put/`` takes 3 querystring parameters:
* ``s3_object_name`` (required) - Name of the file being uploaded
* ``s3_object_type`` (optional) - Content type of the file (e.g. ``application/text``)
* ``s3_object_size`` (optional) - Size of file in bytes

These parameters are then added to the header, so S3 handles the upload appropriately.
It returns JSON:
```json
    { "url": "https://my_domain/my_bucket/my_filename?Signature=xxxx&Expires=xxxx&AWSAccessKeyId=xxxx&x-amz-acl=xxxx" }
```
Errors are returned as JSON:
```json
    { "error": "Authentication failed" }
```

Combine the URL above with a HTTP ``PUT`` request and your file, to upload to S3.
You can customize the bucket name, CORS config, ACL headers and a callback URL, by including
the relevant values in ``settings.py``. See [Settings](#settings) for a full list of settings
available.

