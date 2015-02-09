# StackFormation

 A collection of community templates for [AWS CloudFormation](http://aws.amazon.com/cloudformation/).

## Status

![Lifecycle: retired](https://img.shields.io/badge/lifecycle-retired-blue.svg) ![Support: unsupported](https://img.shields.io/badge/support-unsupported-yellow.svg) ![Maintenance: unmaintained](https://img.shields.io/badge/maintenance-unmaintained-yellow.svg)

This project has been retired and is no longer supported or maintained.
* the project's goal turned out to be inappropriate - CloudFormation templates are best maintained in a target project itself, or a resp. dedicated sidekick project, if need be
* if you should choose to fork it, please let us know so we can link to your project

----

Very early stages, not much to see/use; especially this is mostly about tooling so far, i.e. there are no internal 
[templates](https://github.com/sopel/stackformation/tree/master/templates) migrated here yet - available already are:

* [New Relic Cloudwatch Plugin (spot)](https://github.com/sopel/stackformation/blob/master/templates/newrelic-cloudwatch-plugin-spot.md)

Also, you can play with the tooling by means of the 
[download-aws-cloudformation-samples.py](https://github.com/sopel/stackformation/blob/master/scripts/download-aws-cloudformation-samples.py) helper script.

## Overview

This project aims to be a shared repository hosting community templates for [AWS CloudFormation](http://aws.amazon.com/cloudformation/)
(and eventually [OpenStack Heat](https://github.com/openstack/heat) down the road).

### Background

There's a growing collection of [CloudFormation Sample Templates](http://aws.amazon.com/cloudformation/aws-cloudformation-templates/) provided by AWS itself,
however, these are apparently more geared towards demonstration of available features and also do not seem to be maintained consistently (esp. they are unfortunately
not maintained as Open Source Software (OSS) on GitHub like the [AWS SDKs](http://aws.amazon.com/tools/) for example) - this project aims to complement these offerings.

## Documentation

Please see the [Wiki](https://github.com/sopel/stackformation/wiki) for full documentation, examples and other information.

## License

Licensed under the Apache License, Version 2.0, see LICENSE.TXT for details.
