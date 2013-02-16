#!/usr/bin/env python
"""
Download the AWS CloudFormation sample templates,
which are currently not available alongside the AWS SDKs on GitHub.
"""

import logging
import os
import requests
import sys
import shutil
import xml.etree.ElementTree as ET

# configure default stdout logging handler
log = logging.getLogger('stackformation')
log.setLevel('INFO')
console_handler = logging.StreamHandler()
console_handler.setLevel(log.getEffectiveLevel())
log.addHandler(console_handler)

# pylint: disable=C0111
def main(argv=None):
    if argv is None:
        argv = sys.argv

    # constants
    samples_dir = os.path.abspath(os.path.join(argv[0], os.path.pardir, 
        os.path.pardir, 'templates', 'aws-cloudformation-samples'))
    bucket_url = 'https://s3.amazonaws.com/cloudformation-templates-us-east-1/'

    # delete existing samples directory
    if os.path.exists(samples_dir):
        log.info("Deleting directory '" + samples_dir + "' ...")
        shutil.rmtree(samples_dir)

    # create new samples directory
    os.makedirs(samples_dir)
    log.info("Creating directory '" + samples_dir + "' ...")

    # get and parse bucket listing (an XML ListBucketResult)
    response = requests.get(bucket_url, stream=True)
    tree = ET.parse(response.raw)
    root = tree.getroot()

    # iterate bucket content and download all but HTML files
    log.info("Downloading samples from '" + bucket_url + "' ...")
    for entry in root.iter('{http://s3.amazonaws.com/doc/2006-03-01/}Key'):
        key = entry.text
        if key.endswith('.html'):
            continue

        # get and write file
        log.info("... downloading '" + key + "' ...")
        response = requests.get(bucket_url + key)
        filename = os.path.join(samples_dir, key)
        result = open(filename, 'w')
        result.write(response.content)
        result.close()

if __name__ == '__main__':
    sys.exit(main())
