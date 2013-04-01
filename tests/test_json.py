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
import json
import os
import tests
import stackformation as sfn
import unittest

class TestJSON(unittest.TestCase):

    # REVIEW: this test fails at the first validation error, likely it would be nicer
    # to run each file as a separate test case?
    def test_validate(self):
        for dirpath, dirnames, filenames in os.walk(sfn.templates_dir):
            # validate only *.template files
            for filename in filenames:
                if not filename.endswith('.template'):
                    filenames.remove(filename)

            print "\nValidating ", len(filenames), " templates in ", dirpath, " ..."
            for filename in filenames:
                file = open(os.path.join(dirpath, filename), 'r')
                try:
                    json.load(file)
                except:
                    print "Template '", filename, "' does not validate as JSON:"
                    raise
                finally:
                    file.close()

if __name__ == "__main__":
    unittest.main()
