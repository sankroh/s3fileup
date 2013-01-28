#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os

import boto
from flask import Flask, render_template

app = Flask(__name__)


def generate_bucket_name():
    AWS_STORAGE_BUCKET_NAME = 'app_fileup_assets'

    return AWS_STORAGE_BUCKET_NAME


def generate_signed_url(obj_name, method='GET'):
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    conn = boto.connect_s3(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
        success_action_redirect='http://127.0.0.1:5000/callback/'
    )

    bucket_name = generate_bucket_name()
    try:
        bucket = conn.create_bucket(bucket_name)
    except boto.exception.S3CreateError:
        bucket =conn.lookup(bucket_name)

    # Setting CORS config (Cross Origin Resource)
    cors_cfg = boto.s3.cors.CORSConfiguration()
    cors_cfg.add_rule(['PUT', 'POST', 'DELETE'], 'https://127.0.0.1', allowed_header='*', max_age_seconds=3000, expose_header='x-amz-server-side-encryption')
    cors_cfg.add_rule('GET', '*')
    bucket.set_cors(cors_cfg)

    headers={
        'Content-Type': 'application/octet-stream',
        'x-amz-acl' : 'public-read',
    }

    url = conn.generate_url(300, method, bucket=bucket_name, key=obj_name, headers=headers)

    return url


@app.route('/signs3put')
def put_url():
    url_data = { 'url' : generate_signed_url('testing', method='PUT') }
    return json.loads(url_data)


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
