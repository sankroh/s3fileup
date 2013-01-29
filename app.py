#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.cors import CORSConfiguration
from boto.exception import S3CreateError
from flask import Flask, render_template, request

app = Flask(__name__)


def generate_bucket_name():
    AWS_STORAGE_BUCKET_NAME = 'app_mi_assets'

    return AWS_STORAGE_BUCKET_NAME


def generate_signed_url(obj_name, obj_type, method='GET'):
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    conn = S3Connection(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        calling_format=OrdinaryCallingFormat()
    )

    bucket_name = generate_bucket_name()
    try:
        bucket = conn.create_bucket(bucket_name)
    except S3CreateError:
        bucket =conn.lookup(bucket_name)

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


@app.route('/signs3put')
def put_url():
    # get params from URL
    s3_object_type = request.args.get('s3_object_type', 'application/octet-stream')
    s3_object_name = request.args.get('s3_object_name', 'untitled_file')

    url_data = { 'url' : generate_signed_url(s3_object_name, s3_object_type, method='PUT') }
    return json.dumps(url_data)


@app.route('/callback')
def callback():
    return 'Callback!'


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
