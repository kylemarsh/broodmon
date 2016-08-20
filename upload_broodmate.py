#!/usr/bin/python

import boto
import logging
import sys 
import os

from boto.s3.connection import S3Connection, OrdinaryCallingFormat

logging.basicConfig(level=logging.CRITICAL)

conn = S3Connection(
    host='objects.dreamhost.com',
    is_secure=False,
	calling_format=OrdinaryCallingFormat())

logging.info("Connection to dho established")
bucket = conn.lookup('broodmate')

if not bucket:
    logging.fatal("couldn't find the broodmate bucket!")
    sys.exit(1)

brood_dir = os.path.join('/home', 'pi', 'broodmon')
files = {'graphs': ['hour.png', 'day.png', 'week.png', 'month.png'], 'cam': ['lastsnap.jpg']}

for k in files.keys():
    for f in files[k]:
        filename = os.path.join(brood_dir, k, f)
        logging.info("uploading %s" % filename)
        key = bucket.new_key(f)
        key.set_contents_from_filename(filename, replace=True)
        key.set_canned_acl('public-read')

