#!/usr/bin/env python
"""
This is the StackFormation build script based on Fabric (http://fabfile.org/).
"""
import boto
import boto.cloudformation
import botocross as bc
from fabric.api import local, task
import logging
import nose
import os
import stackformation as sfn

log = logging.getLogger('fabric')
bc.configure_logging(log, 'INFO')

@task(default=True)
def test(args=None):
    """
    Run all tests.

    Specify string argument ``args`` for additional args to ``nosetests``.
    """
    test_unit(args)
    test_integration(args)

@task
def test_integration(args=None):
    """
    Run all integration tests.

    Specify string argument ``args`` for additional args to ``nosetests``.
    """
    default_args = "--nocapture --verbose --nologcapture tests/integration"
    default_args += (" " + args) if args else ""
    nose.core.run(argv=[''] + default_args.split())

@task
def test_unit(args=None):
    """
    Run all unit tests.

    Specify string argument ``args`` for additional args to ``nosetests``.
    """
    default_args = "--nocapture --verbose --nologcapture tests/unit"
    default_args += (" " + args) if args else ""
    nose.core.run(argv=[''] + default_args.split())

@task
def create_buckets(bucket_base_name):
    """
    Create required S3 buckets.
    """
    sfn.create_buckets(bucket_base_name)

@task
def validate_buckets(bucket_base_name):
    """
    Validate that required S3 buckets exist.
    """
    sfn.validate_buckets(bucket_base_name)

@task
def list():
    """
    List templates.
    """
    sfn.list_templates()

@task
def upload(bucket_base_name):
    """
    Upload templates to existing S3 buckets.
    """
    test()
    sfn.upload_templates(bucket_base_name)

@task
def validate_body():
    """
    Validate templates via body upload.
    """
    try:
        cfn = boto.connect_cloudformation()
        for dirpath, dirnames, filenames in os.walk(sfn.TEMPLATES_DIR):
            # upload only *.template files
            filenames = [ filename for filename in filenames if filename.endswith('.template') ]

            print "Validating ", len(filenames), "templates from ", dirpath, " ..."
            for filename in filenames:
                try:
                    with open(os.path.join(dirpath, filename), 'r') as template:
                        response = cfn.validate_template(template_body=template.read())
                except:
                    pass
    except boto.exception.BotoServerError, e:
        log.error(e.error_message)

@task
def validate_url(bucket_base_name):
    """
    Validate templates via URLs of S3 objects.
    """
    regions = boto.cloudformation.regions()
    for region in regions:
        bucket_name = bucket_base_name + '-' + region.name
        try:
            cfn = boto.connect_cloudformation(region=region)
            for dirpath, dirnames, filenames in os.walk(sfn.TEMPLATES_DIR):
                # upload only *.template files
                filenames = [ filename for filename in filenames if filename.endswith('.template') ]

                print "Validating ", len(filenames), "templates in ", bucket_name, " ..."
                for filename in filenames:
                    keyname = os.path.relpath(os.path.join(dirpath, filename)).replace('\\', '/')
                    template_url = "http://s3"
                    # handle S3 legacy issue regarding region 'US Standard', see e.g. 
                    # https://forums.aws.amazon.com/message.jspa?messageID=185820
                    if region.name != 'us-east-1':
                        template_url += ('-' + region.name)
                    template_url += ('.amazonaws.com/' + bucket_name + '/' + keyname)
                    log.info("... validating {0} ...".format(keyname))
                    template = cfn.validate_template(template_url=template_url)
        except boto.exception.BotoServerError, e:
            log.error(e.error_message)

@task
def download_aws_samples():
    """
    Download the AWS CloudFormation sample templates.
    """
    local('python ' + os.path.abspath(os.path.join('.', 'scripts', 'download-aws-cloudformation-samples.py')))
