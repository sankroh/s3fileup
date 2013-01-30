django-s3fileup
===============

S3FileUp is an Apache2 Licensed pluggable Django app that provides you with an
API to upload files to S3 directly from the browser, without the file ever
touching your server.

It's implemented using ``django-tastypie``, so you can reuse any of the Authorization
/Authentication schemes that your webapp uses. There is also an implementation
without any django dependencies, see the [examples](#examples) section for more
info.

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

This app exposes two resource URLs that can be used by the client. Using the example
above, the URLs are ``/uploads/s3/v1/s3put/`` and ``/uploads/s3/v1/s3get/``.

### Get an upload URL

>#### Definition
>``POST /uploads/s3/v1/s3put/``
>
>#### Parameters
>* ``s3_object_name`` (required) - Name of the file being uploaded
>* ``s3_object_type`` (optional) - Content type of the file (e.g. ``application/text``)
>* ``s3_object_size`` (optional) - Size of file in bytes
>
>These parameters are then added to the header, so S3 handles the upload appropriately.
>
>#### Example Request
>```bash
>$ curl https://my_app/uploads/s3/v1/s3put/ \
>  -u my_user \
>  -d "s3_object_name=my_awesome_movie.mov" \
>  -d "s3_object_type=video/quicktime" \
>  -d s3_object_size=3459034
>```
>
>#### Example Response
>```json
>{ "url": "https://my_domain/my_bucket/my_filename?Signature=xxxx&Expires=xxxx&AWSAccessKeyId=xxxx&x-amz-acl=xxxx" }
>```
>Errors are returned as JSON:
>```json
>{ "error": "Authentication failed" }
>```
>
>Combine the URL above with a ``HTTP PUT`` request and your file, to upload to S3.
>You can customize the bucket name, CORS config, ACL headers and a callback URL, by including
>the relevant values in ``settings.py``. See [Settings](#settings) for a full list of settings
>available.

### Get a read-only URL

>Not implemented.

Examples
--------
The ``examples`` folder contains a sample Django app with a JavaScript implementation
of a upload client.

>For those who are Django averse or just want a simple API, there is a sample
[Flask](http://flask.pocoo.org) app in the ``flask`` branch. The Flask app does
not have any auth and has a simpler settings/configuration paradigm.

References
----------
* [How to directly upload files to Amazon S3[..]](http://codeartists.com/post/36892733572/how-to-directly-upload-files-to-amazon-s3-from-your) - ``Code Artists``
* [Direct Browser Uploading – Amazon S3[..]](http://www.ioncannon.net/programming/1539/direct-browser-uploading-amazon-s3-cors-fileapi-xhr2-and-signed-puts/) - ``Carson McDonald``

