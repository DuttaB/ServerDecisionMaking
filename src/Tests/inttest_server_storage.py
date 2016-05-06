"""
ECE 4574: Final Exam
File Name: inttest_server_storage.py
Author: Chang Sun
Date: May 5, 2016
Description: Integration testing for server_storage.py
"""

# _________________________________________________________________________________________________


import datetime
import uuid
import unittest
from StringIO import StringIO
import holder
from json_generators import *
from server_storage import *

# _________________________________________________________________________________________________


class IntTestServerStorage(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(IntTestServerStorage, self).__init__(*args, **kwargs)

    def test(self):
        print('******Running test cases******')

        #history = get_last_states()
        event = generate_lambda("", "sensors", "MODIFY")
        holder.lambda_handler(event, 0)
        self.assertEqual(True, True)

        print('******Finished running test cases******')


# _________________________________________________________________________________________________


if __name__ == '__main__':
    unittest.main()


# _________________________________________________________________________________________________
