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
import json
import os
import stackformation as sfn
import unittest

class TestCloudFormation(unittest.TestCase):
    """
    Test templates via CloudFormation API.
    """
    # REVIEW: this test fails at the first validation error, likely it would be nicer
    # to run each file as a separate test case?
    def test_validate(self):
        """
        Test templates validate via CloudFormation API.
        """
        cfn = boto.connect_cloudformation()
        for dirpath, dirnames, filenames in os.walk(sfn.TEMPLATES_DIR):
            # validate only *.template files
            filenames = [ filename for filename in filenames if filename.endswith('.template') ]

            print "\nValidating ", len(filenames), " templates in ", dirpath, " ..."
            for filename in filenames:
                try:
                    with open(os.path.join(dirpath, filename), 'r') as template:
                        response = cfn.validate_template(template_body=template.read())
                except:
                    print "Template '", filename, "' does not validate in CloudFormation:"
                    raise

if __name__ == "__main__":
    unittest.main()
