# Copyright 2013 Steffen Opel. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import boto
import botocross as bc
import logging
import os.path

__version__ = '0.1.0'
TEMPLATES_DIR = os.path.abspath(os.path.join('.', 'templates'))

# REVIEW: How is the global log variaable handled elsewhere usually?
# pylint: disable=C0103
log = logging.getLogger('stackformation')
# pylint: enable=C0103
bc.configure_logging(log, 'INFO')

# TODO: this modules entire functionality should be migrated upstream to botocross,
# which currently doesn't provide the loop on a package level, rather only in the scripts!
def loop_locations(fn, bucket_base_name):
    """
    Loop over all S3 locations and execute function fn.
    """
    from botocross.s3 import RegionMap, class_iterator
    
    s3 = boto.connect_s3()
    locations = class_iterator(boto.s3.connection.Location)
    for location in locations:
        region = RegionMap[location]
        bucket_name = bucket_base_name + '-' + region
        try:
            fn(s3, bucket_name, location=getattr(boto.s3.connection.Location, location))
        except boto.exception.BotoServerError, e:
            log.error(e.error_message)

def create_buckets(bucket_base_name):
    """
    Create S3 buckets.
    """

    def create_bucket(s3, bucket_name, location):
        """
        Create S3 bucket.
        """
        log.info("Creating bucket {0} ...".format(bucket_name))
        s3.create_bucket(bucket_name, location=location)

    loop_locations(create_bucket, bucket_base_name)

def validate_buckets(bucket_base_name):
    """
    Validate that S3 buckets exist.
    """

    # pylint: disable=W0613
    def validate_bucket(s3, bucket_name, location=None):
        """
        Validate that required S3 buckets exist.
        """
        log.info("Validating bucket {0} ...".format(bucket_name))
        if None is s3.lookup(bucket_name):
            log.warn("... bucket {0} does not exist!".format(bucket_name))
        else:
            log.info("... bucket {0} is available.".format(bucket_name))

    loop_locations(validate_bucket, bucket_base_name)

def list_templates(templates_dir=TEMPLATES_DIR):
    """
    List available templates.
    """

    for dirpath, dirnames, filenames in os.walk(templates_dir):
        # list only *.template files
        filenames = [ filename for filename in filenames if filename.endswith('.template') ]

    log.info("There are {0} templates within {1} ...".format(len(filenames), dirpath))
    for filename in filenames:
        name = os.path.relpath(os.path.join(dirpath, filename)).replace('\\', '/')
        log.info("... {0} ...".format(name))

def upload_templates(bucket_base_name, templates_dir=TEMPLATES_DIR):
    """
    Upload templates to existing S3 buckets.
    """

    def upload_template(s3, bucket_name, location=None):
        """
        Upload template to existing S3 buckets.
        """
        bucket = s3.get_bucket(bucket_name)
        key = boto.s3.key.Key(bucket)
        for dirpath, dirnames, filenames in os.walk(templates_dir):
            # upload only *.template files
            filenames = [ filename for filename in filenames if filename.endswith('.template') ]

            log.info("Uploading {0} templates from {1} to {2} ...".format(len(filenames), dirpath, bucket_name))
            for filename in filenames:
                key.name = os.path.relpath(os.path.join(dirpath, filename)).replace('\\', '/')
                log.debug("... uploading {0} ...".format(key.name))
                key.set_contents_from_filename(os.path.join(dirpath, filename))

    loop_locations(upload_template, bucket_base_name)
