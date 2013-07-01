# StackFormation: New Relic Cloudwatch Plugin

## Purpose

This [AWS CloudFormation](http://aws.amazon.com/cloudformation/) template starts a single 
[EC2 Spot Instance](http://aws.amazon.com/ec2/spot-instances/) via Auto Scaling from an upstream maintained EBS AMI 
of the [New Relic Cloudwatch Plugin](https://aws.amazon.com/marketplace/pp/B00DMMUO0O?sr=0-31&qid=1372405347838):

* Template: [New Relic Cloudwatch Plugin (spot)](https://github.com/sopel/stackformation/blob/master/templates/newrelic-cloudwatch-plugin-spot.template)

## Parameters

There are a few required and optional parameters as follows:

* Please note that due to the plugin being supposed to run in an ongoing fashion across all AWS regions, 
an Auto Scaling notification topic ARN is assembled from a therefore required AWS account number and SNS topic.

```json
    "Parameters": {
        "AccountNumber": {
            "Type": "String",
            "Description": "AWS account number to build region specific ARN for Auto Scaling notifications."
        },
        "AutoScalingTopic": {
            "Type": "String",
            "Description": "SNS topic to build region specific ARN for Auto Scaling notifications."
        },
        "InstanceProfile": {
            "Type": "String",
            "Description": "IAM instance profile to use within the Auto Scaling group."
        },
        "InstanceType": {
            "Description": "EC2 instance type",
            "Type": "String",
            "Default": "t1.micro",
            "AllowedValues": [
                "t1.micro",
                "m1.small",
                "m1.medium",
                "c1.medium"
            ],
            "ConstraintDescription": "must be a valid (and allowed) EC2 instance type."
        },
        "KeyName": {
            "Description": "Name of an existing EC2 key pair to enable remote access.",
            "Type": "String"
        },
        "NewRelicLicenseKey": {
            "Description": "New Relic account license key.",
            "Type": "String"
        },
        "RemoteAccessCidrIp": {
            "Description": "CIDR range to allow remote access from (default: localhost, i.e. none).",
            "Type": "String",
            "Default": "127.0.0.1/32"
        },
        "SpotPrice": {
            "Type": "Number",
            "Description": "Spot price for instances to start within the Auto Scaling group.",
            "Default": "0.012"
        }
    }
```

## AMIs

The current AMI ids are based on version 1 of the plugin (as released on the AWS Marketplace) and will need to be updated 
for each subsequent release:

```json
        "RegionMap": {
            "us-east-1": {
                "AMI": "ami-cf0979a6"
            },
            "us-west-1": {
                "AMI": "ami-0c381149"
            },
            "us-west-2": {
                "AMI": "ami-3b4ada0b"
            },
            "eu-west-1": {
                "AMI": "ami-79ccde0d"
            },
            "ap-southeast-1": {
                "AMI": "ami-541a5306"
            },
            "ap-southeast-2": {
                "AMI": "ami-a342d199"
            },
            "ap-northeast-1": {
                "AMI": "ami-c54dc7c4"
            },
            "sa-east-1": {
                "AMI": "ami-c86bced5"
            }
        }
```
