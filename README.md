django-s3fileup
===============

S3FileUp is an Apache2 Licensed pluggable Django app that provides you with an
API to upload files to S3 directly from the browser, without the file ever
touching your server.

It's implemented using ``django-restframework``, so you can reuse any of the Authorization
/Authentication schemes that your webapp uses. There is also an implementation
without any django dependencies, see the [examples](#examples) section for more
info.

3rd Party Requirements
----------------------

* boto==2.7.0
* django-restframework==2.3.6

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

* **S3FILEUP_GENERATE_BUCKET** : Indicate if you want to create a new bucket,
  defaults to ``False``.

* **S3FILEUP_BUCKET_PREFIX** : Prefix for a new bucket. The suffix is auto-generated
  from the current datetime and is of the format ``%Y_%m_%d_%H_%M``. This only
  required if ``S3FILEUP_GENERATE_BUCKET`` is set to ``True``.

* **S3FILEUP_BUCKET_NAME** : S3 Bucket name to use. This is only required if ``S3FILEUP_GENERATE_BUCKET``
  is set to ``False``.

* **S3FILEUP_DOMAIN** : Domain you will be uploading from. This is used to set CORS
  configs on the bucket, so that cross-domain upload requests are allowed.

* **S3FILEUP_MAX_AGE** : Define the max age of the url that is generated,
  defaults to ``3000``. The value is in seconds.

Usage
-----

This app exposes one resource URLs that can be used by the client. Using the example
above, the URL is ``/uploads/s3/s3put/``.

### Get an upload URL

>#### Definition
>``POST /uploads/s3/s3put/``
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
>$ curl https://my_app/uploads/s3/s3put/ \
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


Examples
--------
The ``examples`` folder contains a sample Django app with a JavaScript implementation
of a upload client.

>For those who prefer django-tastypie over django-restframework, there is a
working implementation in the ``tastypie`` branch.

>For those who are Django averse or just want a simple API, there is a sample
[Flask](http://flask.pocoo.org) app in the ``flask`` branch. The Flask app does
not have any auth and has a simpler settings/configuration paradigm.

References
----------
* [How to directly upload files to Amazon S3[..]](http://codeartists.com/post/36892733572/how-to-directly-upload-files-to-amazon-s3-from-your) - ``Code Artists``
* [Direct Browser Uploading – Amazon S3[..]](http://www.ioncannon.net/programming/1539/direct-browser-uploading-amazon-s3-cors-fileapi-xhr2-and-signed-puts/) - ``Carson McDonald``

